"""Pytest configuration and fixtures."""
import pytest
from django.conf import settings
from rest_framework.test import APIClient

from apps.users.models import User


@pytest.fixture
def api_client():
    """Return API client."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        telegram_id=123456789,
        username="testuser",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return User.objects.create_superuser(
        telegram_id=987654321,
        username="admin",
        first_name="Admin",
        last_name="User",
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Return authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Return admin authenticated API client."""
    api_client.force_authenticate(user=admin_user)
    return api_client
