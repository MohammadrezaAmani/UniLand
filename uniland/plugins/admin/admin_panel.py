from pyrogram import Client, filters

import uniland.db.user_methods as user_db
from uniland.utils.builders import Builder
from uniland.utils.filters import access_level, exact_match, user_step
from uniland.utils.steps import UserSteps
from uniland.utils.triggers import Triggers
from uniland.utils.uxhandler import UXTree


@Client.on_message(
    filters.text
    & user_step(UserSteps.START.value)
    & exact_match(Triggers.ADMIN_PANEL.value)
    & access_level(min=2)
)
async def admin_panel(client, message):
    """
    This function handles the admin panel functionality.

    Args:
        client: The client object.
        message: The message object.
    """
    user_step = UXTree.nodes[UserSteps.ADMIN_PANEL.value]
    text, keyboard = Builder.display_panel(message.from_user.id)
    await message.reply(text, reply_markup=keyboard)
    user_db.update_user_step(message.from_user.id, user_step.step)


# TODO use admin_panel instead of display_panel in other files?
