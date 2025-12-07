"""User service for bot operations."""
import logging
from typing import Optional

from asgiref.sync import sync_to_async
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

from apps.users.models import User

logger = logging.getLogger(__name__)


class UserService:
    """Service for user-related operations."""

    CACHE_TTL = 3600  # 1 hour

    def _get_cache_key(self, telegram_id: int) -> str:
        """Get cache key for user."""
        return f"user:{telegram_id}"

    @sync_to_async
    def get_or_create_user(self, telegram_id: int, **user_data) -> User:
        """Get or create user from Telegram data."""
        cache_key = self._get_cache_key(telegram_id)
        user = cache.get(cache_key)

        if user is None:
            user, created = User.objects.get_or_create(
                telegram_id=telegram_id,
                defaults={
                    "username": user_data.get("username"),
                    "first_name": user_data.get("first_name", ""),
                    "last_name": user_data.get("last_name", ""),
                    "language_code": user_data.get("language_code", "fa"),
                },
            )

            if not created:
                # Update user info if changed
                updated = False
                for field in ["username", "first_name", "last_name"]:
                    if field in user_data and getattr(user, field) != user_data[field]:
                        setattr(user, field, user_data[field])
                        updated = True

                if updated:
                    user.save()

            cache.set(cache_key, user, self.CACHE_TTL)
            logger.info(f"User {'created' if created else 'retrieved'}: {telegram_id}")

        return user

    @sync_to_async
    def update_user_activity(self, telegram_id: int):
        """Update user's last activity timestamp."""
        User.objects.filter(telegram_id=telegram_id).update(last_active=timezone.now())
        cache.delete(self._get_cache_key(telegram_id))

    @sync_to_async
    def update_user_step(self, telegram_id: int, step: str):
        """Update user's current step."""
        User.objects.filter(telegram_id=telegram_id).update(last_step=step)
        cache.delete(self._get_cache_key(telegram_id))

    @sync_to_async
    def get_user(self, telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID."""
        cache_key = self._get_cache_key(telegram_id)
        user = cache.get(cache_key)

        if user is None:
            try:
                user = User.objects.get(telegram_id=telegram_id)
                cache.set(cache_key, user, self.CACHE_TTL)
            except User.DoesNotExist:
                return None

        return user

    @sync_to_async
    def check_permission(self, telegram_id: int, min_level: int = 1) -> bool:
        """Check if user has minimum permission level."""
        user = cache.get(self._get_cache_key(telegram_id))
        if user is None:
            try:
                user = User.objects.get(telegram_id=telegram_id)
            except User.DoesNotExist:
                return False

        return user.has_permission(min_level)

    @sync_to_async
    def get_user_step(self, telegram_id: int) -> str:
        """Get user's current step."""
        user = cache.get(self._get_cache_key(telegram_id))
        if user is None:
            try:
                user = User.objects.get(telegram_id=telegram_id)
            except User.DoesNotExist:
                return "start_stage"

        return user.last_step

    @sync_to_async
    @transaction.atomic
    def update_user_stats(self, telegram_id: int, submissions_delta: int = 0, likes_delta: int = 0):
        """Update user statistics."""
        user = User.objects.select_for_update().get(telegram_id=telegram_id)
        user.total_submissions += submissions_delta
        user.total_likes_received += likes_delta
        user.update_score()
        cache.delete(self._get_cache_key(telegram_id))
