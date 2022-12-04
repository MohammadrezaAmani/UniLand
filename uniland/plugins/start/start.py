# Adding users to database and navigate to bot's branches
from pyrogram import Client, filters
from uniland import usercache
import uniland.db.user_methods as user_db
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXNode, UXTree


@Client.on_message(filters.private & filters.command("start"))
async def start_stage(client, message):
    if not usercache.has_user(message.from_user.id):
        user_db.add_user(user_id=message.from_user.id, last_step=UserSteps.START.value)

    start_step = UXTree.nodes[UserSteps.START.value]
    await message.reply(
        text=start_step.description,
        reply_markup=start_step.keyboard,
    )
    user_db.update_user_step(message.from_user.id, start_step.step)
