"""Search URLs."""
from django.urls import path

from . import views

app_name = "search"

urlpatterns = [
    path("", views.SearchView.as_view(), name="search"),
    path("popular/", views.PopularSearchesView.as_view(), name="popular"),
]
