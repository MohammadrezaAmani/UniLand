"""Start command handler."""
import logging

from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup

from apps.bot.di import get_injector
from apps.bot.services.user_service import UserService
from apps.bot.utils.keyboards import get_main_keyboard
from apps.bot.utils.messages import Messages

logger = logging.getLogger(__name__)
injector = get_injector()
user_service = injector.get(UserService)


@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """Handle /start command."""
    # Get or create user
    user = await user_service.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name or "",
        last_name=message.from_user.last_name or "",
        language_code=message.from_user.language_code or "fa",
    )

    # Update activity and step
    await user_service.update_user_activity(message.from_user.id)
    await user_service.update_user_step(message.from_user.id, "start_stage")

    # Get appropriate keyboard based on user permissions
    keyboard = await get_main_keyboard(user.access_level)

    # Send welcome message
    welcome_text = Messages.get_welcome_message(user.first_name or "کاربر")

    await message.reply(
        welcome_text,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )

    logger.info(f"User {message.from_user.id} started the bot")
