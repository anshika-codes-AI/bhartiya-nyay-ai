from django.urls import path
from .views import DraftTypeListView, DraftCreateView,DraftFactIntakeView

urlpatterns = [
    path("draft-types/", DraftTypeListView.as_view()),
    path("drafts/create/", DraftCreateView.as_view()),
    path("drafts/<int:draft_id>/facts/", DraftFactIntakeView.as_view()),
]