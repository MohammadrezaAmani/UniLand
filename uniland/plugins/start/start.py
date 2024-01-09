from pyrogram import Client, filters

import uniland.db.user_methods as user_db
from uniland import usercache
from uniland.utils.filters import user_exists
from uniland.utils.pages import Pages
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree


@Client.on_message(~user_exists, group=1)
async def handle_new_user(client, message):
    """
    Handles new user messages and adds the user to the database.

    Args:
        client (TelegramClient): The Telegram client instance.
        message (Message): The incoming message.

    Returns:
        None
    """
    try:
        user_db.add_user(message.from_user.id, last_step=UserSteps.START.value)
    except:
        pass


@Client.on_message(filters.text & filters.command("start") & filters.private)
async def user_entrance(client, message):
    """
    Handles the user entrance when they send a private message with the "/start" command.

    Args:
        client: The Telegram client.
        message: The message object containing user information.
    """
    user_id = message.from_user.id
    if not usercache.has_user(user_id):
        user_db.add_user(user_id, last_step=UserSteps.START.value)

    custom_message = f"سلام {message.from_user.first_name} عزیز"
    custom_message += "\nبه بات UniLand خوش اومدی!"

    start_step = UXTree.nodes[UserSteps.START.value]
    if usercache.has_permission(user_id, min_permission=2, max_permission=3):
        await message.reply(text=custom_message, reply_markup=Pages.ADMIN_HOME)
    else:
        await message.reply(text=custom_message, reply_markup=start_step.keyboard)
    user_db.update_user_step(user_id, start_step.step)


async def start_stage(client, message):
    """
    This function handles the start stage of the bot.

    Parameters:
        client (TelegramClient): The Telegram client object.
        message (Message): The message object received from the user.
    """
    user_id = message.from_user.id
    if not usercache.has_user(user_id):
        user_db.add_user(user_id, last_step=UserSteps.START.value)

    custom_message = f"ممنون که همراه مایی {message.from_user.first_name} عزیز، دیگه چه کاری می‌تونم برات انجام بدم؟"

    start_step = UXTree.nodes[UserSteps.START.value]
    if usercache.has_permission(user_id, min_permission=2, max_permission=3):
        await message.reply(text=custom_message, reply_markup=Pages.ADMIN_HOME)
    else:
        await message.reply(text=custom_message, reply_markup=start_step.keyboard)
    user_db.update_user_step(user_id, start_step.step)


@Client.on_message(group=2)
async def update_last_activity_on_message(client, message):
    """
    Update the last activity of a user when a message is received.

    Args:
        client: The client instance.
        message: The message received.

    Returns:
        None
    """
    try:
        if not usercache.has_user(message.from_user.id):
            user_db.add_user(message.from_user.id, last_step=UserSteps.START.value)
        user_db.update_user_activity(message.from_user.id)
    except:
        pass


@Client.on_callback_query(group=2)
async def update_last_activity_on_callback(client, callback_query):
    """
    Updates the last activity of a user when a callback query is received.

    Args:
        client: The client object.
        callback_query: The callback query object.
    """
    try:
        if not usercache.has_user(callback_query.from_user.id):
            user_db.add_user(
                callback_query.from_user.id, last_step=UserSteps.START.value
            )
        user_db.update_user_activity(callback_query.from_user.id)
    except:
        pass


@Client.on_inline_query(group=2)
async def update_last_activity_on_inline(client, inline_query):
    """
    Updates the last activity of the user when an inline query is received.

    Parameters:
        client (Client): The client instance.
        inline_query (InlineQuery): The inline query received.
    """
    try:
        if not usercache.has_user(inline_query.from_user.id):
            user_db.add_user(inline_query.from_user.id, last_step=UserSteps.START.value)
        user_db.update_user_activity(inline_query.from_user.id)
    except:
        pass
