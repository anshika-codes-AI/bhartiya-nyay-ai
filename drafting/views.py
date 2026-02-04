from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Draft, DraftType
from .serializers import DraftCreateSerializer, DraftTypeSerializer

from .models import DraftFact
from .services import transition_draft
from drafting.workflow import DraftStatus
from .serializers import DraftFactIntakeSerializer


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
                {"error": "Facts already submitted"},
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