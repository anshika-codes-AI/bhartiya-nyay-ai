from django.shortcuts import render
from drafting.draft_generation import generate_draft_blueprint
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Draft, DraftType
from .serializers import DraftCreateSerializer, DraftTypeSerializer
from drafting.models import DraftLegalMapping
from .models import DraftFact
from .services import transition_draft
from drafting.workflow import DraftStatus
from .serializers import DraftFactIntakeSerializer

from transition_engine.services import map_ipc_to_bns

from drafting.ai_drafting import generate_ai_draft
from drafting.docx_export import export_draft_to_docx
from drafting.models import DraftContent
class DraftTypeListView(APIView):
    def get(self, request):
        draft_types = DraftType.objects.all()
        serializer = DraftTypeSerializer(draft_types, many=True)
        return Response(serializer.data)


class DraftCreateView(APIView):
    def post(self, request):
        serializer = DraftCreateSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            draft = serializer.save()
            return Response(
                {"id": draft.id, "status": draft.status},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DraftFactIntakeView(APIView):
    def post(self, request, draft_id):
        try:
            draft = Draft.objects.get(id=draft_id, user=request.user)
        except Draft.DoesNotExist:
            return Response(
                {"error": "Draft not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Only allow fact intake at CREATED stage
        if draft.status != DraftStatus.CREATED.value:
            return Response(
                {"error": "Draft is no longer in CREATED state"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = DraftFactIntakeSerializer(
            data=request.data,
            context={"draft": draft}
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save facts
        for fact in serializer.validated_data["facts"]:
            DraftFact.objects.create(
                draft=draft,
                key=fact["key"],
                value=fact["value"]
            )

        # Transition workflow
        transition_draft(draft, DraftStatus.FACTS_COLLECTED)

        return Response(
            {"status": draft.status},
            status=status.HTTP_200_OK
        )
    
class DraftLegalMappingView(APIView):
    def post(self, request, draft_id):
        try:
            draft = Draft.objects.get(
                id=draft_id,
                user=request.user
            )
        except Draft.DoesNotExist:
            return Response(
                {"error": "Draft not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if draft.status != DraftStatus.FACTS_COLLECTED.value:
            return Response(
                {"error": "Facts not collected yet"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract IPC sections from facts
        facts = {f.key: f.value for f in draft.facts.all()}
        raw_sections = facts.get("SECTIONS_INVOKED", [])

        if isinstance(raw_sections, str):
            # handle comma-separated or single value
            sections = [s.strip() for s in raw_sections.split(",")]
        else:
            sections = raw_sections

        mappings = map_ipc_to_bns(sections)
        
        if not mappings:
            return Response(
                {"error": "No mappings found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if draft.legal_mappings.exists():
            return Response(
                {"error": "Legal mapping already completed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Save mapping to DB
        for mapping in mappings:
            DraftLegalMapping.objects.create(
                draft=draft,
                ipc_section=mapping.ipc_section,
                bns_section=mapping.bns_section,
                intent=mapping.intent,
                drafting_note=mapping.drafting_note
            )
        # Transition workflow
        transition_draft(draft, DraftStatus.LEGAL_MAPPED)

        return Response(
            {
                "status": draft.status,
                "legal_basis": [
                    {
                        "ipc": str(m.ipc_section),
                        "bns": str(m.bns_section),
                        "intent": m.intent,
                        "drafting_note": m.drafting_note,
                    }
                    for m in draft.legal_mappings.all()
                ]
            },
            status=status.HTTP_200_OK
        )
class DraftGenerateView(APIView):
    def post(self, request, draft_id):
        try:
            draft = Draft.objects.get(
                id=draft_id,
                user=request.user
            )
        except Draft.DoesNotExist:
            return Response(
                {"error": "Draft not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            blueprint = generate_draft_blueprint(draft)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "status": draft.status,
                "draft_blueprint": blueprint
            },
            status=status.HTTP_200_OK
        )

class DraftAIDraftingView(APIView):
    def post(self, request, draft_id):
        try:
            draft = Draft.objects.get(
                id=draft_id,
                user=request.user
            )
        except Draft.DoesNotExist:
            return Response(
                {"error": "Draft not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            blueprint = {
                "facts": {f.key: f.value for f in draft.facts.all()},
                "legal_basis": [
                    {
                        "ipc": str(m.ipc_section),
                        "bns": str(m.bns_section),
                        "intent": m.intent
                    }
                    for m in draft.legal_mappings.all()
                ]
            }

            ai_text = generate_ai_draft(draft, blueprint)
            latest_version = draft.contents.count() + 1

            DraftContent.objects.create(
                draft=draft,
                content=ai_text,
                version=latest_version
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "status": draft.status,
                "draft_text": ai_text
            },
            status=status.HTTP_200_OK
        )
class DraftExportView(APIView):
    def post(self, request, draft_id):
        try:
            draft = Draft.objects.get(
                id=draft_id,
                user=request.user
            )
        except Draft.DoesNotExist:
            return Response(
                {"error": "Draft not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        latest_content = draft.contents.order_by("-version").first()

        if not latest_content:
            return Response(
                {"error": "No draft content available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        draft_text = latest_content.content

        if not draft_text:
            return Response(
                {"error": "Draft text required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            path = export_draft_to_docx(draft, draft_text)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "status": draft.status,
                "file_path": path
            },
            status=status.HTTP_200_OK
        )