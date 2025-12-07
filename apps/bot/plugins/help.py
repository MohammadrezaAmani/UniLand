"""Help command handler with multi-language support."""
import logging
from copy import deepcopy

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from apps.bot.di import get_injector
from apps.bot.services.user_service import UserService
from apps.bot.utils.messages import Messages

logger = logging.getLogger(__name__)
injector = get_injector()
user_service = injector.get(UserService)


def get_help_keyboard(lang: str = "fa", selected: int = 0):
    """Get help menu keyboard with selected button highlighted."""
    buttons = [
        [InlineKeyboardButton("🏠 صفحه اصلی" if lang == "fa" else "🏠 Home", callback_data="help:menu")],
        [InlineKeyboardButton("🔎 راهنمای جستجو" if lang == "fa" else "🔎 Search Guide", callback_data="help:search")],
        [InlineKeyboardButton("📤 راهنمای ثبت فایل" if lang == "fa" else "📤 Submit Guide", callback_data="help:submit")],
        [InlineKeyboardButton("🎰 امتیازگیری" if lang == "fa" else "🎰 Scoring", callback_data="help:scores")],
        [InlineKeyboardButton("🦸‍♂️ درباره ما" if lang == "fa" else "🦸‍♂️ About Us", callback_data="help:about")],
        [InlineKeyboardButton("🔜 بزودی..." if lang == "fa" else "🔜 Coming Soon", callback_data="help:soon")],
    ]
    
    if selected > 0:
        custom_buttons = deepcopy(buttons)
        custom_buttons[selected][0].text = "👈 " + custom_buttons[selected][0].text
        return custom_buttons
    
    return buttons


@Client.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
    """Handle /help command."""
    user = await user_service.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name or "",
        last_name=message.from_user.last_name or "",
        language_code=message.from_user.language_code or "fa",
    )
    
    lang = user.language_code
    help_text = Messages.get("help", lang)
    
    await message.reply(
        help_text,
        reply_markup=InlineKeyboardMarkup(get_help_keyboard(lang, 0)),
    )


@Client.on_callback_query(filters.regex(r"^help:"))
async def help_callback(client: Client, callback_query):
    """Handle help menu callbacks."""
    action = callback_query.data.split(":")[1]
    
    user = await user_service.get_user(callback_query.from_user.id)
    lang = user.language_code if user else "fa"
    
    messages_map = {
        "menu": ("help", 0),
        "search": ("help_search", 1),
        "submit": ("help_submit", 2),
        "scores": ("help_scores", 3),
        "about": ("help_about", 4),
        "soon": ("help_soon", 5),
    }
    
    if action in messages_map:
        msg_key, selected = messages_map[action]
        text = Messages.get(msg_key, lang)
        await callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(get_help_keyboard(lang, selected)),
        )
    
    await callback_query.answer()
