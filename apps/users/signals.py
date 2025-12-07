"""User signals."""
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import User

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """Handle user post-save signal."""
    if created:
        logger.info(f"New user created: {instance.telegram_id}")
        # Add any post-creation logic here
