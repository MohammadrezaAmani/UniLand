"""Celery tasks for bot operations."""
import logging

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from apps.bot.client import TelegramClient
from apps.users.models import User

logger = logging.getLogger(__name__)


@shared_task
def cleanup_old_sessions():
    """Clean up old bot sessions."""
    logger.info("Cleaning up old sessions...")
    # Implementation for session cleanup
    return "Sessions cleaned"


@shared_task
def broadcast_message_task(user_ids: list, text: str, **kwargs):
    """Broadcast message to multiple users asynchronously."""
    import asyncio

    client = TelegramClient()

    async def _broadcast():
        await client.start()
        results = await client.broadcast_message(user_ids, text, **kwargs)
        await client.stop()
        return results

    results = asyncio.run(_broadcast())
    logger.info(f"Broadcast completed: {results['success']} success, {results['failed']} failed")
    return results


@shared_task
def send_notification_to_admins(message: str):
    """Send notification to all admin users."""
    admin_ids = list(
        User.objects.filter(
            access_level=User.AccessLevel.ADMIN,
            is_active=True,
        ).values_list("telegram_id", flat=True)
    )

    if admin_ids:
        broadcast_message_task.delay(admin_ids, f"🔔 Admin Notification\n\n{message}")

    return f"Notification sent to {len(admin_ids)} admins"


@shared_task
def update_user_scores():
    """Update all user scores."""
    users = User.objects.all()
    updated = 0

    for user in users:
        user.update_score()
        updated += 1

    logger.info(f"Updated scores for {updated} users")
    return f"Updated {updated} user scores"
