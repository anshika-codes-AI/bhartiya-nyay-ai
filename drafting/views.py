import os
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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .serializers import DraftCreateSerializer

from drafting.authentication import CsrfExemptSessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drafting.models import Draft, DraftContent
from drafting.docx_export import export_draft_to_docx
from rest_framework.response import Response


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def draft_preview_page(request):
    return render(request, "draft_preview.html")

    
@method_decorator(csrf_exempt, name="dispatch")
class DraftCreateView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]

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
@method_decorator(csrf_exempt, name="dispatch")
class DraftAIDraftingView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]
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
            draft.status = DraftStatus.DRAFT_GENERATED.value
            draft.save()
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
    authentication_classes = []
    permission_classes = []

    def post(self, request, draft_id):
        try:
            draft = Draft.objects.get(id=draft_id)

            latest_content = (
                DraftContent.objects
                .filter(draft=draft)
                .order_by("-version")
                .first()
            )

            if not latest_content:
                return Response(
                    {"error": "No draft content found"},
                    status=400
                )

            file_path = export_draft_to_docx(
                draft,
                latest_content.content
            )

            if not os.path.exists(file_path):
                return Response(
                    {"error": "DOCX file not created"},
                    status=500
                )

            return FileResponse(
                open(file_path, "rb"),
                as_attachment=True,
                filename=f"Bhartiya_Nyay_Draft_{draft.id}.docx"
            )

        except Exception as e:
            print("EXPORT ERROR:", e)
            return Response(
                {"error": str(e)},
                status=500
            )