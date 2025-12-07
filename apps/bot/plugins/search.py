"""PV search handler."""
import logging

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from apps.bot.di import get_injector
from apps.bot.services.submission_service import SubmissionService
from apps.bot.services.user_service import UserService
from apps.bot.utils.keyboards import get_back_keyboard, get_main_keyboard
from apps.search.services import SearchService

logger = logging.getLogger(__name__)
injector = get_injector()
user_service = injector.get(UserService)
search_service = injector.get(SearchService)
submission_service = injector.get(SubmissionService)

# Store user search state
user_search_state = {}


@Client.on_message(filters.regex(r"^🔍 جستجو 🔎$") & filters.private)
async def start_search(client: Client, message: Message):
    """Start search flow."""
    user = await user_service.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name or "",
        last_name=message.from_user.last_name or "",
    )
    
    await user_service.update_user_step(message.from_user.id, "bot_pv_search")
    
    user_search_state[message.from_user.id] = True
    
    lang = user.language_code
    text = "لطفا متن جستجو را وارد کنید:" if lang == "fa" else "Please enter your search query:"
    
    from pyrogram.types import ReplyKeyboardMarkup
    await message.reply(text, reply_markup=ReplyKeyboardMarkup(get_back_keyboard(), resize_keyboard=True))


@Client.on_message(filters.text & filters.private)
async def handle_search_query(client: Client, message: Message):
    """Handle search query input."""
    # Check if user is in search state
    if message.from_user.id not in user_search_state:
        return
    
    # Check for back button
    if message.text == "🔙 برگشت":
        user_search_state.pop(message.from_user.id, None)
        await user_service.update_user_step(message.from_user.id, "start_stage")
        
        user = await user_service.get_user(message.from_user.id)
        keyboard = await get_main_keyboard(user.access_level if user else 1)
        
        from pyrogram.types import ReplyKeyboardMarkup
        await message.reply(
            "بازگشت به منوی اصلی" if user.language_code == "fa" else "Back to main menu",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        return
    
    query = message.text.strip()
    
    if len(query) > 100:
        await message.reply("متن جستجو بیش از حد طولانی است." if message.from_user.language_code == "fa" else "Search query is too long.")
        return
    
    if len(query) < 2:
        await message.reply("متن جستجو بیش از حد کوتاه است." if message.from_user.language_code == "fa" else "Search query is too short.")
        return
    
    # Perform search
    ignored, results = await search_service.search(query, limit=50)
    
    if not results:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("جستجوی اینلاین", switch_inline_query_current_chat="")]
        ])
        await message.reply(
            "🕶️ نگران نباش! داریم دنبال فایلت می‌گردیم و به زودی به بات اضافه می‌شه.\n"
            "در ضمن حتما یه سری به نحوه سرچ در بات که توی قسمت راهنما هست بزن! "
            "شاید فایلی که می‌خوای رو داشته باشیم ولی درست جستجوش نکردی.",
            reply_markup=keyboard
        )
        return
    
    # Display results with pagination
    page = 0
    page_size = 5
    await display_search_results(message, query, results, page, page_size)


async def display_search_results(message, query: str, results: list, page: int, page_size: int):
    """Display paginated search results."""
    start = page * page_size
    end = min(start + page_size, len(results))
    page_results = results[start:end]
    
    text = f"🌐 نتایج جستجو برای {query}\n\n"
    text += f"نتایج {start + 1} تا {end} از {len(results)} رکورد\n\n"
    
    for idx, submission in enumerate(page_results, start=start + 1):
        text += f"📔 رکورد {idx}:\n"
        if hasattr(submission, 'user_display'):
            text += submission.user_display()
        text += f"\n👍 مورد علاقه {submission.likes_count} نفر\n"
        text += f"📥 دریافت رکورد: /get_{submission.submission_type}_{submission.id}\n"
        text += "─" * 25 + "\n\n"
    
    # Navigation buttons
    buttons = []
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⏮ صفحه قبل", callback_data=f"search:{page-1}:{page_size}:{query}"))
    if end < len(results):
        nav_row.append(InlineKeyboardButton("صفحه بعد ⏭", callback_data=f"search:{page+1}:{page_size}:{query}"))
    
    if nav_row:
        buttons.append(nav_row)
    
    await message.reply(
        text,
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
        parse_mode=ParseMode.DISABLED
    )


@Client.on_callback_query(filters.regex(r"^search:"))
async def search_pagination(client: Client, callback_query):
    """Handle search pagination."""
    parts = callback_query.data.split(":", 3)
    page = int(parts[1])
    page_size = int(parts[2])
    query = parts[3]
    
    if page < 0:
        await callback_query.answer("این صفحه اول است.", show_alert=True)
        return
    
    # Perform search again
    ignored, results = await search_service.search(query, limit=50)
    
    if page * page_size >= len(results):
        await callback_query.answer("این صفحه آخر است.", show_alert=True)
        return
    
    start = page * page_size
    end = min(start + page_size, len(results))
    page_results = results[start:end]
    
    text = f"نتایج جستجو برای {query}\n\n"
    text += f"نتایج {start + 1} تا {end} از {len(results)} رکورد\n\n"
    
    for idx, submission in enumerate(page_results, start=start + 1):
        text += f"📔 رکورد {idx}:\n"
        if hasattr(submission, 'user_display'):
            text += submission.user_display()
        text += f"\n👍 مورد علاقه {submission.likes_count} نفر\n"
        text += f"📥 دریافت رکورد: /get_{submission.submission_type}_{submission.id}\n"
        text += "─" * 25 + "\n\n"
    
    # Navigation buttons
    buttons = []
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⏮ صفحه قبل", callback_data=f"search:{page-1}:{page_size}:{query}"))
    if end < len(results):
        nav_row.append(InlineKeyboardButton("صفحه بعد ⏭", callback_data=f"search:{page+1}:{page_size}:{query}"))
    
    if nav_row:
        buttons.append(nav_row)
    
    await callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
        parse_mode=ParseMode.DISABLED
    )


@Client.on_message(filters.regex(r"^/get_") & filters.private)
async def get_submission(client: Client, message: Message):
    """Handle /get_type_id command to retrieve submissions."""
    try:
        parts = message.text.split("_")
        submission_type = parts[1]
        submission_id = int(parts[2])
        
        submission = await submission_service.get_submission(submission_id)
        
        if not submission or not submission.is_confirmed:
            await message.reply("این رکورد وجود ندارد.")
            return
        
        # Increment search times
        from asgiref.sync import sync_to_async
        from django.db import models as django_models
        from apps.submissions.models import Submission
        
        @sync_to_async
        def increment_search():
            Submission.objects.filter(id=submission_id).update(search_times=django_models.F('search_times') + 1)
        
        await increment_search()
        
        # Send the submission
        from apps.bot.utils.keyboards import get_bookmark_keyboard
        
        if submission_type == "document":
            from apps.submissions.models import Document
            doc = await sync_to_async(Document.objects.get)(id=submission_id)
            await message.reply_document(
                document=doc.file_id,
                caption=doc.user_display() + "\n\n@UniLandBot",
                reply_markup=get_bookmark_keyboard(submission.id, submission.likes_count)
            )
        elif submission_type == "profile":
            from apps.submissions.models import Profile
            profile = await sync_to_async(Profile.objects.get)(id=submission_id)
            if profile.image_id:
                await message.reply_document(
                    document=profile.image_id,
                    caption=profile.user_display() + "\n\n@UniLandBot",
                    reply_markup=get_bookmark_keyboard(submission.id, submission.likes_count)
                )
            else:
                await message.reply_text(
                    text=profile.user_display() + "\n\n@UniLandBot",
                    reply_markup=get_bookmark_keyboard(submission.id, submission.likes_count)
                )
        elif submission_type == "media":
            from apps.submissions.models import Media
            media = await sync_to_async(Media.objects.get)(id=submission_id)
            await message.reply_text(
                text=media.user_display() + "\n\n@UniLandBot",
                reply_markup=get_bookmark_keyboard(submission.id, submission.likes_count)
            )
    
    except Exception as e:
        logger.error(f"Error retrieving submission: {e}")
        await message.reply("خطا در دریافت محتوا.")
