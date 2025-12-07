"""Tests for user models and views."""
import pytest
from django.urls import reverse

from apps.users.models import User


@pytest.mark.django_db
class TestUserModel:
    """Test User model."""

    def test_create_user(self):
        """Test creating a user."""
        user = User.objects.create_user(
            telegram_id=123456789,
            username="testuser",
            first_name="Test",
        )
        assert user.telegram_id == 123456789
        assert user.username == "testuser"
        assert user.access_level == User.AccessLevel.ORDINARY

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            telegram_id=987654321,
            username="admin",
        )
        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.access_level == User.AccessLevel.ADMIN

    def test_user_score_calculation(self):
        """Test user score calculation."""
        user = User.objects.create_user(telegram_id=123456789)
        user.total_submissions = 5
        user.total_likes_received = 10
        user.update_score()
        assert user.score == 35  # (5 * 5) + 10

    def test_has_permission(self):
        """Test permission checking."""
        user = User.objects.create_user(telegram_id=123456789)
        assert user.has_permission(User.AccessLevel.ORDINARY) is True
        assert user.has_permission(User.AccessLevel.EDITOR) is False


@pytest.mark.django_db
class TestUserViews:
    """Test user API views."""

    def test_get_current_user(self, authenticated_client, user):
        """Test getting current user."""
        url = reverse("users:me")
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert response.data["telegram_id"] == user.telegram_id

    def test_get_user_stats(self, authenticated_client, user):
        """Test getting user statistics."""
        url = reverse("users:stats")
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert "score" in response.data
        assert "total_submissions" in response.data

    def test_unauthorized_access(self, api_client):
        """Test unauthorized access."""
        url = reverse("users:me")
        response = api_client.get(url)
        assert response.status_code == 401
