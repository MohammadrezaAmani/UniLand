"""Callback query handlers."""
import logging

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from apps.bot.di import get_injector
from apps.bot.services.submission_service import SubmissionService
from apps.bot.services.user_service import UserService
from apps.bot.utils.keyboards import get_bookmark_keyboard

logger = logging.getLogger(__name__)
injector = get_injector()
user_service = injector.get(UserService)
submission_service = injector.get(SubmissionService)


@Client.on_callback_query(filters.regex(r"^bookmark:"))
async def toggle_bookmark_callback(client: Client, callback_query: CallbackQuery):
    """Handle bookmark toggle callback."""
    try:
        _, sub_id, likes = callback_query.data.split(":")
        sub_id, likes = int(sub_id), int(likes)

        # Get or create user
        user = await user_service.get_or_create_user(
            telegram_id=callback_query.from_user.id,
            username=callback_query.from_user.username,
            first_name=callback_query.from_user.first_name or "",
            last_name=callback_query.from_user.last_name or "",
        )

        # Toggle bookmark
        result, new_likes = await submission_service.toggle_bookmark(user, sub_id)

        if result == 0:
            await callback_query.answer("Something went wrong!", show_alert=True)
        elif result == 1:
            await callback_query.answer("Added to bookmarks ✅")
        else:
            await callback_query.answer("Removed from bookmarks ❌")

        # Update button if likes changed
        if new_likes != likes:
            await callback_query.edit_message_reply_markup(
                reply_markup=get_bookmark_keyboard(sub_id, new_likes)
            )

    except Exception as e:
        logger.error(f"Error toggling bookmark: {e}")
        await callback_query.answer("Error occurred", show_alert=True)


@Client.on_callback_query(filters.regex(r"^confirm:"))
async def confirm_submission_callback(client: Client, callback_query: CallbackQuery):
    """Handle submission confirmation callback."""
    try:
        _, sub_id = callback_query.data.split(":")
        sub_id = int(sub_id)

        # Check permission
        has_permission = await user_service.check_permission(callback_query.from_user.id, min_level=2)
        if not has_permission:
            await callback_query.answer("You don't have permission!", show_alert=True)
            return

        # Get user
        user = await user_service.get_user(callback_query.from_user.id)

        # Confirm submission
        success = await submission_service.confirm_submission(sub_id, user)

        if success:
            await callback_query.answer("Submission confirmed! ✅")
            await callback_query.edit_message_text(
                callback_query.message.text + "\n\n✅ CONFIRMED"
            )
        else:
            await callback_query.answer("Failed to confirm submission", show_alert=True)

    except Exception as e:
        logger.error(f"Error confirming submission: {e}")
        await callback_query.answer("Error occurred", show_alert=True)


@Client.on_callback_query(filters.regex(r"^reject:"))
async def reject_submission_callback(client: Client, callback_query: CallbackQuery):
    """Handle submission rejection callback."""
    try:
        _, sub_id = callback_query.data.split(":")
        sub_id = int(sub_id)

        # Check permission
        has_permission = await user_service.check_permission(callback_query.from_user.id, min_level=2)
        if not has_permission:
            await callback_query.answer("You don't have permission!", show_alert=True)
            return

        # Delete submission
        success = await submission_service.delete_submission(sub_id)

        if success:
            await callback_query.answer("Submission rejected! ❌")
            await callback_query.edit_message_text(
                callback_query.message.text + "\n\n❌ REJECTED"
            )
        else:
            await callback_query.answer("Failed to reject submission", show_alert=True)

    except Exception as e:
        logger.error(f"Error rejecting submission: {e}")
        await callback_query.answer("Error occurred", show_alert=True)
