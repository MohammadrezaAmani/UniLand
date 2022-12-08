# Adding users to database and navigate to bot's branches
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import uniland.db.user_methods as user_db
from uniland.utils.triggers import Triggers
from uniland.utils.messages import Messages
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree
from uniland.utils.uxhandler import UXTree
from uniland.utils.filters import user_step, exact_match
from copy import deepcopy

buttons = \
    [
        [
            InlineKeyboardButton(  # Opens a web URL
                "صفحه اصلی",
                callback_data="helpmenu:back_to_help_menu"
            ),
        ],
        [
            InlineKeyboardButton(  # Opens a web URL
                "راهنمای جستجو",
                callback_data="helpemenu:display_search_details"
            ),
        ],
        [
            InlineKeyboardButton(  # Opens a web URL
                "راهنمای ثبت فایل",
                callback_data="helpemenu:display_submit_details"
            ),
        ],
        [
            InlineKeyboardButton(  # Opens a web URL
                "درباره ما",
                callback_data="helpemenu:display_about_us"
            ),
        ],
        [
            InlineKeyboardButton(  # Opens a web URL
                "بزودی...",
                callback_data="helpemenu:display_coming_soon"
            ),
        ]
    ]

# Generate the new keyboard with selected button


def get_keyboard(index: int):
    custom_buttons = deepcopy(buttons)
    custom_buttons[index][0].text = " 👈 " + custom_buttons[index][0].text
    return custom_buttons


@Client.on_message(filters.text &
                   user_step(UserSteps.START.value) & exact_match(Triggers.HELP.value))
async def display_help_menu(client, message):
    await message.reply(text=Messages.HELP_MENU.value,
                        reply_markup=InlineKeyboardMarkup(get_keyboard(0)))


@Client.on_callback_query(filters.regex('helpmenu:back_to_help_menu'))
async def back_to_menu(client, callback_query):
    await callback_query.edit_message_text(Messages.HELP_MENU.value)
    await callback_query.edit_message_reply_markup(
        InlineKeyboardMarkup(get_keyboard(0))
    )


@Client.on_callback_query(filters.regex('helpemenu:display_search_details'))
async def search_help(client, callback_query):
    await callback_query.edit_message_text(Messages.HELP_MENU_SEARCH.value)
    await callback_query.edit_message_reply_markup(
        InlineKeyboardMarkup(get_keyboard(1))
    )


@Client.on_callback_query(filters.regex('helpemenu:display_submit_details'))
async def submit_help(client, callback_query):
    await callback_query.edit_message_text(Messages.HELP_MENU_SUBMIT.value)
    await callback_query.edit_message_reply_markup(
        InlineKeyboardMarkup(get_keyboard(2))
    )


@Client.on_callback_query(filters.regex('helpemenu:display_about_us'))
async def about_us(client, callback_query):
    await callback_query.edit_message_text(Messages.HELP_MENU_ABOUT_US.value)
    await callback_query.edit_message_reply_markup(
        InlineKeyboardMarkup(get_keyboard(3))
    )


@Client.on_callback_query(filters.regex('helpemenu:display_coming_soon'))
async def coming_soon(client, callback_query):
    await callback_query.edit_message_text(Messages.HELP_MENU_COMING_SOON.value)
    await callback_query.edit_message_reply_markup(
        InlineKeyboardMarkup(get_keyboard(4))
    )
