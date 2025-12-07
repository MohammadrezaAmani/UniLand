"""Submission signals."""
import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.submissions.models import Bookmark, Submission

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Submission)
def submission_post_save(sender, instance, created, **kwargs):
    """Handle submission post-save signal."""
    if created:
        logger.info(f"New submission created: {instance.id} by {instance.owner.telegram_id}")
        # Update user stats
        instance.owner.total_submissions += 1
        instance.owner.update_score()

    if instance.is_confirmed and not created:
        # Index for search
        from apps.search.services import SearchService
        import asyncio

        search_service = SearchService()
        asyncio.create_task(search_service.index_submission(instance))


@receiver(post_delete, sender=Submission)
def submission_post_delete(sender, instance, **kwargs):
    """Handle submission post-delete signal."""
    logger.info(f"Submission deleted: {instance.id}")
    # Remove from search index
    from apps.search.services import SearchService
    import asyncio

    search_service = SearchService()
    asyncio.create_task(search_service.remove_from_index(instance.id))


@receiver(post_save, sender=Bookmark)
def bookmark_created(sender, instance, created, **kwargs):
    """Handle bookmark creation."""
    if created:
        # Update submission likes count
        instance.submission.likes_count += 1
        instance.submission.save(update_fields=["likes_count"])

        # Update owner stats
        owner = instance.submission.owner
        owner.total_likes_received += 1
        owner.update_score()


@receiver(post_delete, sender=Bookmark)
def bookmark_deleted(sender, instance, **kwargs):
    """Handle bookmark deletion."""
    # Update submission likes count
    instance.submission.likes_count -= 1
    instance.submission.save(update_fields=["likes_count"])

    # Update owner stats
    owner = instance.submission.owner
    owner.total_likes_received -= 1
    owner.update_score()
