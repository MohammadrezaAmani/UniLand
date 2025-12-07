"""Keyboard utilities for bot."""
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton

from apps.users.models import User


async def get_main_keyboard(access_level: int = 1) -> list:
    """Get main menu keyboard based on user access level."""
    keyboard = [
        [KeyboardButton("🔍 جستجو 🔎")],
        [KeyboardButton("📤 ارسال محتوا 📤")],
        [KeyboardButton("👩‍💻 پروفایل من 👨‍💻"), KeyboardButton("📜 راهنما 📜")],
    ]

    # Add admin panel for editors and admins
    if access_level >= User.AccessLevel.EDITOR:
        keyboard.append([KeyboardButton("دسترسی‌های ویژه")])

    return keyboard


def get_back_keyboard() -> list:
    """Get back button keyboard."""
    return [[KeyboardButton("🔙 برگشت")]]


def get_submission_type_keyboard() -> list:
    """Get submission type selection keyboard."""
    return [
        [KeyboardButton("ارسال فایل")],
        [KeyboardButton("ارسال اطلاعات")],
        [KeyboardButton("ارسال رسانه")],
        [KeyboardButton("🔙 برگشت")],
    ]


def get_document_type_keyboard() -> InlineKeyboardMarkup:
    """Get document type selection keyboard."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("کتاب", callback_data="doctype:book"),
                InlineKeyboardButton("جزوه", callback_data="doctype:pamphlet"),
            ],
            [
                InlineKeyboardButton("تمرینات", callback_data="doctype:exercises"),
                InlineKeyboardButton("تمپلیت", callback_data="doctype:template"),
            ],
            [InlineKeyboardButton("ترکیبی", callback_data="doctype:compressed")],
        ]
    )


def get_confirmation_keyboard(submission_id: int) -> InlineKeyboardMarkup:
    """Get submission confirmation keyboard."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ تایید", callback_data=f"confirm:{submission_id}"),
                InlineKeyboardButton("❌ رد", callback_data=f"reject:{submission_id}"),
            ],
            [InlineKeyboardButton("✏️ ویرایش", callback_data=f"edit:{submission_id}")],
        ]
    )


def get_bookmark_keyboard(submission_id: int, likes: int) -> InlineKeyboardMarkup:
    """Get bookmark button keyboard."""
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(f"👍 {likes}", callback_data=f"bookmark:{submission_id}:{likes}")]]
    )


def get_pagination_keyboard(
    page: int, total_pages: int, callback_prefix: str
) -> InlineKeyboardMarkup:
    """Get pagination keyboard."""
    buttons = []

    if page > 0:
        buttons.append(InlineKeyboardButton("⏮ قبلی", callback_data=f"{callback_prefix}:{page-1}"))

    buttons.append(InlineKeyboardButton(f"{page + 1}/{total_pages}", callback_data="noop"))

    if page < total_pages - 1:
        buttons.append(InlineKeyboardButton("بعدی ⏭", callback_data=f"{callback_prefix}:{page+1}"))

    return InlineKeyboardMarkup([buttons])
