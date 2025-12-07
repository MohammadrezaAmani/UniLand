"""Submission service for bot operations."""
import logging
from typing import List, Optional

from asgiref.sync import sync_to_async
from django.db import transaction

from apps.submissions.models import Bookmark, Document, Media, Profile, Submission
from apps.users.models import User

logger = logging.getLogger(__name__)


class SubmissionService:
    """Service for submission-related operations."""

    @sync_to_async
    @transaction.atomic
    def create_document(self, owner: User, **data) -> Document:
        """Create a new document submission."""
        document = Document.objects.create(
            owner=owner,
            submission_type=Submission.SubmissionType.DOCUMENT,
            **data
        )

        # Auto-confirm if user is editor or admin
        if owner.access_level >= User.AccessLevel.EDITOR:
            document.confirm(owner)

        return document

    @sync_to_async
    @transaction.atomic
    def create_profile(self, owner: User, **data) -> Profile:
        """Create a new profile submission."""
        profile = Profile.objects.create(
            owner=owner,
            submission_type=Submission.SubmissionType.PROFILE,
            **data
        )

        if owner.access_level >= User.AccessLevel.EDITOR:
            profile.confirm(owner)

        return profile

    @sync_to_async
    @transaction.atomic
    def create_media(self, owner: User, **data) -> Media:
        """Create a new media submission."""
        media = Media.objects.create(
            owner=owner,
            submission_type=Submission.SubmissionType.MEDIA,
            **data
        )

        if owner.access_level >= User.AccessLevel.EDITOR:
            media.confirm(owner)

        return media

    @sync_to_async
    def get_submission(self, submission_id: int) -> Optional[Submission]:
        """Get submission by ID."""
        try:
            return Submission.objects.select_related("owner", "confirmed_by").get(id=submission_id)
        except Submission.DoesNotExist:
            return None

    @sync_to_async
    def get_unconfirmed_submissions(self) -> List[Submission]:
        """Get all unconfirmed submissions."""
        return list(
            Submission.objects.filter(is_confirmed=False, is_deleted=False)
            .select_related("owner")
            .order_by("-created_at")
        )

    @sync_to_async
    @transaction.atomic
    def toggle_bookmark(self, user: User, submission_id: int) -> tuple:
        """Toggle bookmark for a submission."""
        try:
            submission = Submission.objects.select_for_update().get(id=submission_id)
        except Submission.DoesNotExist:
            return (0, 0)  # Something went wrong

        bookmark, created = Bookmark.objects.get_or_create(user=user, submission=submission)

        if not created:
            # Bookmark exists, remove it
            bookmark.delete()
            submission.likes_count -= 1
            submission.save(update_fields=["likes_count"])
            return (-1, submission.likes_count)  # Removed
        else:
            # Bookmark created
            submission.likes_count += 1
            submission.save(update_fields=["likes_count"])
            return (1, submission.likes_count)  # Added

    @sync_to_async
    def get_user_bookmarks(self, user: User, limit: int = 50) -> List[Submission]:
        """Get user's bookmarked submissions."""
        return list(
            Submission.objects.filter(
                submission_bookmarks__user=user,
                is_confirmed=True,
                is_deleted=False,
            )
            .select_related("owner")
            .order_by("-submission_bookmarks__created_at")[:limit]
        )

    @sync_to_async
    def get_user_submissions(self, user: User, limit: int = 50) -> List[Submission]:
        """Get user's submissions."""
        return list(
            Submission.objects.filter(owner=user, is_deleted=False)
            .select_related("confirmed_by")
            .order_by("-created_at")[:limit]
        )

    @sync_to_async
    @transaction.atomic
    def confirm_submission(self, submission_id: int, admin: User) -> bool:
        """Confirm a submission."""
        try:
            submission = Submission.objects.select_for_update().get(id=submission_id)
            submission.confirm(admin)
            return True
        except (Submission.DoesNotExist, PermissionError) as e:
            logger.error(f"Failed to confirm submission {submission_id}: {e}")
            return False

    @sync_to_async
    @transaction.atomic
    def delete_submission(self, submission_id: int) -> bool:
        """Soft delete a submission."""
        try:
            submission = Submission.objects.get(id=submission_id)
            submission.soft_delete()
            return True
        except Submission.DoesNotExist:
            return False
