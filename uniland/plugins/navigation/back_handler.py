from pyrogram import Client, filters
from uniland.utils import triggers, uxhandler
from uniland import usercache
import uniland.db.user_methods as user_db
from uniland.utils.steps import UserSteps
from uniland.plugins.start.start import start_stage
from uniland.utils.builders import Builder


@Client.on_message(filters.regex(triggers.Triggers.BACK.value) & filters.private)
async def back_nav(client, message):
    step = usercache.get_last_step(message.from_user.id)
    user_step = uxhandler.UXTree.nodes[step]
    if step == UserSteps.START.value:
        return
    if user_step.parent.step == UserSteps.START.value:
        await start_stage(client, message)
    elif user_step.parent.step == UserSteps.ADMIN_PANEL.value:
        text, keyboard = Builder.display_panel(message.from_user.id)
        await message.reply(text, reply_markup=keyboard)
        user_db.update_user_step(message.from_user.id, user_step.parent.step)
    else:
        await message.reply(
            text=user_step.parent.description, reply_markup=user_step.parent.keyboard
        )
        user_db.update_user_step(message.from_user.id, user_step.parent.step)
