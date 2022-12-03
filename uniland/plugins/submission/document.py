# Implementing finctionality of users' document submission

from pyrogram import Client, filters
import pyrogram
from uniland.utils import messages
import uniland.db.user_methods as user_db
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree


@Client.on_message(filters.regex(messages.Messages.DOCUMENT.value))
async def submmition_handler(
    client: pyrogram.client.Client,
    message: pyrogram.types.messages_and_media.message.Message,
):
    step = UXTree.nodes[UserSteps.DOCUMENT_SUBMISSION.value]
    user_db.update_user_step(message.from_user.id, UserSteps.DOCUMENT_SUBMISSION.value)
    await message.reply(text=str(step.trigger), reply_markup=step.keyboard)
