from pyrogram import Client, filters
import pyrogram
from uniland.utils import messages, uxhandler
from uniland import usercache
import uniland.db.user_methods as user_db
from uniland.utils.steps import UserSteps


#! complete this section
@Client.on_message(filters.regex(messages.Messages.BACK.value))
async def document_handler(client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
    step = user_db.get_user(message.from_user.id).last_step
    parent = uxhandler.UXTree.nodes[step]
    if parent != UserSteps.START:
      pass
    await message.reply(
            text='اه',
        )

