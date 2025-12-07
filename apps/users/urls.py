"""User URLs."""
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("me/", views.CurrentUserView.as_view(), name="me"),
    path("me/stats/", views.UserStatsView.as_view(), name="stats"),
    path("<int:telegram_id>/", views.UserDetailView.as_view(), name="detail"),
]
