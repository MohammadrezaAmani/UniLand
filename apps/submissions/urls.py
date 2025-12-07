"""Submission URLs."""
from django.urls import path

from . import views

app_name = "submissions"

urlpatterns = [
    path("", views.SubmissionListView.as_view(), name="list"),
    path("<int:pk>/", views.SubmissionDetailView.as_view(), name="detail"),
    path("pending/", views.PendingSubmissionsView.as_view(), name="pending"),
    path("<int:pk>/confirm/", views.ConfirmSubmissionView.as_view(), name="confirm"),
    path("<int:pk>/reject/", views.RejectSubmissionView.as_view(), name="reject"),
]
