# Adding users to database and navigate to bot's branches
from copy import deepcopy

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from uniland.utils.filters import exact_match, user_step
from uniland.utils.messages import Messages
from uniland.utils.steps import UserSteps
from uniland.utils.triggers import Triggers

buttons = [
    [
        InlineKeyboardButton(  # Opens a web URL
            " صفحه اصلی 🏠", callback_data="helpmenu:back_to_help_menu"
        ),
    ],
    [
        InlineKeyboardButton(  # Opens a web URL
            " راهنمای جستجو 🔎", callback_data="helpemenu:display_search_details"
        ),
    ],
    [
        InlineKeyboardButton(  # Opens a web URL
            " راهنمای ثبت فایل 📤", callback_data="helpemenu:display_submit_details"
        ),
    ],
    [
        InlineKeyboardButton(  # Opens a web URL
            " امتیازگیری 🎰", callback_data="helpemenu:display_scores"
        ),
    ],
    [
        InlineKeyboardButton(  # Opens a web URL
            " درباره ما 🦸‍♂️", callback_data="helpemenu:display_about_us"
        ),
    ],
    [
        InlineKeyboardButton(  # Opens a web URL
            "بزودی... 🔜", callback_data="helpemenu:display_coming_soon"
        ),
    ],
]


# Generate the new keyboard with selected button highlighted
def get_keyboard(index: int):
    """
    Returns a modified version of the buttons list with the specified index button text modified.

    Args:
        index (int): The index of the button to modify.

    Returns:
        list: A modified version of the buttons list with the specified index button text modified.
    """
    custom_buttons = deepcopy(buttons)
    custom_buttons[index][0].text = " 👈 " + custom_buttons[index][0].text
    return custom_buttons


@Client.on_message(
    (filters.text & user_step(UserSteps.START.value) & exact_match(Triggers.HELP.value))
    | (filters.text & filters.command("help"))
)
async def display_help_menu(client, message):
    """
    Display the help menu in response to the user's request for help.

    Parameters:
    - client: The client object.
    - message: The message object.

    Returns:
    - None
    """
    await message.reply(
        text=Messages.HELP_MENU.value,
        reply_markup=InlineKeyboardMarkup(get_keyboard(0)),
    )


@Client.on_callback_query(filters.regex("helpmenu:back_to_help_menu"))
async def back_to_menu(client, callback_query):
    """
    Callback function to handle the 'back_to_help_menu' button in the help menu.

    Args:
        client: The Telegram client.
        callback_query: The callback query object.
    """
    await callback_query.edit_message_text(
        Messages.HELP_MENU.value, reply_markup=InlineKeyboardMarkup(get_keyboard(0))
    )


@Client.on_callback_query(filters.regex("helpemenu:display_search_details"))
async def search_help(client, callback_query):
    """
    Display search help menu.

    Args:
        client: The client object.
        callback_query: The callback query object.

    Returns:
        None
    """
    await callback_query.edit_message_text(
        Messages.HELP_MENU_SEARCH.value,
        reply_markup=InlineKeyboardMarkup(get_keyboard(1)),
    )


@Client.on_callback_query(filters.regex("helpemenu:display_submit_details"))
async def submit_help(client, callback_query):
    """
    Display the help menu for submitting details.

    Args:
        client: The client object.
        callback_query: The callback query object.

    Returns:
        None
    """
    await callback_query.edit_message_text(
        Messages.HELP_MENU_SUBMIT.value,
        reply_markup=InlineKeyboardMarkup(get_keyboard(2)),
    )


@Client.on_callback_query(filters.regex("helpemenu:display_scores"))
async def scores_help(client, callback_query):
    """
    Display the help menu for scores.

    Args:
        client: The Telegram client.
        callback_query: The callback query.

    Returns:
        None
    """
    await callback_query.edit_message_text(
        Messages.HELP_MENU_SCORES.value,
        reply_markup=InlineKeyboardMarkup(get_keyboard(3)),
    )


@Client.on_callback_query(filters.regex("helpemenu:display_about_us"))
async def about_us(client, callback_query):
    """
    Display information about us in the help menu.

    Args:
        client: The client object.
        callback_query: The callback query object.

    Returns:
        None
    """
    await callback_query.edit_message_text(
        Messages.HELP_MENU_ABOUT_US.value,
        reply_markup=InlineKeyboardMarkup(get_keyboard(4)),
    )


@Client.on_callback_query(filters.regex("helpemenu:display_coming_soon"))
async def coming_soon(client, callback_query):
    """
    Display a message indicating that the help menu is coming soon.

    Args:
        client: The client object.
        callback_query: The callback query object.

    Returns:
        None
    """
    await callback_query.edit_message_text(
        Messages.HELP_MENU_COMING_SOON.value,
        reply_markup=InlineKeyboardMarkup(get_keyboard(5)),
    )
