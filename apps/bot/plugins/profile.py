"""User profile handler."""
import logging

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from apps.bot.di import get_injector
from apps.bot.services.submission_service import SubmissionService
from apps.bot.services.user_service import UserService
from apps.bot.utils.messages import Messages
from apps.submissions.models import Bookmark

logger = logging.getLogger(__name__)
injector = get_injector()
user_service = injector.get(UserService)
submission_service = injector.get(SubmissionService)


@Client.on_message(filters.command("profile") & filters.private)
async def profile_command(client: Client, message: Message):
    """Handle /profile command."""
    user = await user_service.get_user(message.from_user.id)
    
    if not user:
        await message.reply("User not found. Please start the bot first with /start")
        return
    
    # Get user statistics
    from asgiref.sync import sync_to_async
    
    @sync_to_async
    def get_bookmarks_count():
        return Bookmark.objects.filter(user=user).count()
    
    bookmarks_count = await get_bookmarks_count()
    
    access_level_map = {
        1: "کاربر عادی" if user.language_code == "fa" else "Ordinary User",
        2: "ویرایشگر" if user.language_code == "fa" else "Editor",
        3: "ادمین" if user.language_code == "fa" else "Admin",
    }
    
    profile_text = Messages.get_profile_message(
        score=user.score,
        submissions=user.total_submissions,
        bookmarks=bookmarks_count,
        access_level=access_level_map.get(user.access_level, "Unknown"),
        lang=user.language_code,
    )
    
    buttons = [
        [InlineKeyboardButton(
            "🔖 نمایش پسندها" if user.language_code == "fa" else "🔖 Show Bookmarks",
            callback_data=f"profile:bookmarks:{message.from_user.id}:0"
        )],
        [InlineKeyboardButton(
            "🗄️ نمایش فایل‌های من" if user.language_code == "fa" else "🗄️ My Submissions",
            callback_data=f"profile:submissions:{message.from_user.id}:0"
        )],
    ]
    
    await message.reply(profile_text, reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex(r"^profile:"))
async def profile_callback(client: Client, callback_query):
    """Handle profile callbacks."""
    parts = callback_query.data.split(":")
    action = parts[1]
    user_id = int(parts[2])
    page = int(parts[3]) if len(parts) > 3 else 0
    
    user = await user_service.get_user(user_id)
    lang = user.language_code if user else "fa"
    
    if action == "bookmarks":
        bookmarks = await submission_service.get_user_bookmarks(user, limit=100)
        
        if not bookmarks:
            await callback_query.answer(
                "شما هنوز محتوایی را پسند نکرده‌اید." if lang == "fa" else "You haven't bookmarked any content yet.",
                show_alert=True
            )
            return
        
        # Paginate results
        page_size = 5
        start = page * page_size
        end = start + page_size
        page_items = bookmarks[start:end]
        
        text = "🔖 پسندهای شما\n\n" if lang == "fa" else "🔖 Your Bookmarks\n\n"
        text += f"نتایج {start + 1} تا {min(end, len(bookmarks))} از {len(bookmarks)}\n\n" if lang == "fa" else f"Results {start + 1} to {min(end, len(bookmarks))} of {len(bookmarks)}\n\n"
        
        for idx, sub in enumerate(page_items, start=start + 1):
            text += f"📔 رکورد {idx}:\n" if lang == "fa" else f"📔 Record {idx}:\n"
            if hasattr(sub, 'user_display'):
                text += sub.user_display() + "\n"
            text += f"👍 {sub.likes_count}\n"
            text += f"/get_{sub.submission_type}_{sub.id}\n"
            text += "─" * 25 + "\n\n"
        
        # Navigation buttons
        buttons = []
        nav_row = []
        if page > 0:
            nav_row.append(InlineKeyboardButton("⏮ قبلی" if lang == "fa" else "⏮ Previous", callback_data=f"profile:bookmarks:{user_id}:{page-1}"))
        if end < len(bookmarks):
            nav_row.append(InlineKeyboardButton("بعدی ⏭" if lang == "fa" else "Next ⏭", callback_data=f"profile:bookmarks:{user_id}:{page+1}"))
        
        if nav_row:
            buttons.append(nav_row)
        
        buttons.append([InlineKeyboardButton("🔙 بازگشت" if lang == "fa" else "🔙 Back", callback_data="profile:back")])
        
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    
    elif action == "submissions":
        submissions = await submission_service.get_user_submissions(user, limit=100)
        
        if not submissions:
            await callback_query.answer(
                "شما هنوز محتوایی ثبت نکرده‌اید." if lang == "fa" else "You haven't submitted any content yet.",
                show_alert=True
            )
            return
        
        # Paginate results
        page_size = 5
        start = page * page_size
        end = start + page_size
        page_items = submissions[start:end]
        
        text = "🗄️ فایل‌های ثبت شده توسط شما\n\n" if lang == "fa" else "🗄️ Your Submissions\n\n"
        text += f"نتایج {start + 1} تا {min(end, len(submissions))} از {len(submissions)}\n\n" if lang == "fa" else f"Results {start + 1} to {min(end, len(submissions))} of {len(submissions)}\n\n"
        
        types_fa = {"document": "فایل", "profile": "پروفایل", "media": "رسانه"}
        types_en = {"document": "Document", "profile": "Profile", "media": "Media"}
        types = types_fa if lang == "fa" else types_en
        
        for idx, sub in enumerate(page_items, start=start + 1):
            status = "✅" if sub.is_confirmed else "❌"
            text += f"{status} {types.get(sub.submission_type, sub.submission_type)}:\n"
            if hasattr(sub, 'user_display'):
                text += sub.user_display() + "\n"
            text += "─" * 25 + "\n\n"
        
        # Navigation buttons
        buttons = []
        nav_row = []
        if page > 0:
            nav_row.append(InlineKeyboardButton("⏮ قبلی" if lang == "fa" else "⏮ Previous", callback_data=f"profile:submissions:{user_id}:{page-1}"))
        if end < len(submissions):
            nav_row.append(InlineKeyboardButton("بعدی ⏭" if lang == "fa" else "Next ⏭", callback_data=f"profile:submissions:{user_id}:{page+1}"))
        
        if nav_row:
            buttons.append(nav_row)
        
        buttons.append([InlineKeyboardButton("🔙 بازگشت" if lang == "fa" else "🔙 Back", callback_data="profile:back")])
        
        await callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    
    elif action == "back":
        # Go back to profile main menu
        await profile_command(client, callback_query.message)
    
    await callback_query.answer()
