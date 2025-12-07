"""Choose submission type handler."""
import logging

from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup

from apps.bot.di import get_injector
from apps.bot.services.user_service import UserService

logger = logging.getLogger(__name__)
injector = get_injector()
user_service = injector.get(UserService)


@Client.on_message(filters.regex(r"^📤 ارسال محتوا 📤$") & filters.private)
async def choose_submission_type(client: Client, message: Message):
    """Handle submission type selection."""
    await user_service.update_user_step(message.from_user.id, "submission_type_stage")
    
    keyboard = [
        ["ارسال فایل"],
        ["ارسال اطلاعات"],
        ["🔙 برگشت"],
    ]
    
    text = "لطفا نوع محتوای ارسالی خود را مشخص کنید:\n(توضیح مختصر این بخش را در راهنمای ربات مطالعه نمایید.)"
    
    await message.reply(
        text,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )
