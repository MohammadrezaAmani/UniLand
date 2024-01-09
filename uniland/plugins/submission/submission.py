from pyrogram import Client, filters

import uniland.db.user_methods as user_db
from uniland.utils import triggers
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree


@Client.on_message(filters.regex(triggers.Triggers.SUBMIT.value))
async def submmition_handler(
    client,
    message,
):
    step = UXTree.nodes[UserSteps.CHOOSE_SUBMISSION_TYPE.value]
    user_db.update_user_step(
        message.from_user.id, UserSteps.CHOOSE_SUBMISSION_TYPE.value
    )
    await message.reply(text=str(step.trigger), reply_markup=step.keyboard)
