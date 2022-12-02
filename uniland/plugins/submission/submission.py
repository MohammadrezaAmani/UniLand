from pyrogram import Client, filters
import pyrogram
from uniland.utils import messages, uxhandler
from uniland import usercache
import uniland.db.user_methods as user_db
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree

#! complete this section
@Client.on_message(filters.regex(messages.Messages.SUBMIT.value))
async def submmition_handler(client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
    step = UXTree().nodes[UserSteps.CHOOSE_SUBMISSION_TYPE.value]
    # update last step
    
    await message.reply(
            text=step.trigger,
            
        )

