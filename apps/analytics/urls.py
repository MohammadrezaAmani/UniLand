"""Analytics URLs."""
from django.urls import path

from . import views

app_name = "analytics"

urlpatterns = [
    path("stats/", views.StatisticsView.as_view(), name="stats"),
    path("leaderboard/", views.LeaderboardView.as_view(), name="leaderboard"),
]
