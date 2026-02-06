from django.urls import path
from .views import DraftTypeListView, DraftCreateView,DraftFactIntakeView,DraftLegalMappingView,DraftGenerateView, DraftAIDraftingView,DraftExportView
from .views import draft_preview_page
urlpatterns = [
    path("draft-types/", DraftTypeListView.as_view()),
    path("drafts/create/", DraftCreateView.as_view()),
    path("drafts/<int:draft_id>/facts/", DraftFactIntakeView.as_view()),
    path(
    "drafts/<int:draft_id>/map-law/",
    DraftLegalMappingView.as_view()),
    path(
        "drafts/<int:draft_id>/generate/",
        DraftGenerateView.as_view()
    ),
    path(
    "drafts/<int:draft_id>/ai-draft/",
    DraftAIDraftingView.as_view()
),
path(
    "drafts/<int:draft_id>/export/",
    DraftExportView.as_view()
),
path("drafts/preview/", draft_preview_page),

]