from pyrogram import Client, filters
import pyrogram
from uniland.utils import messages, uxhandler
from uniland import usercache
import uniland.db.user_methods as user_db
from uniland.utils.steps import UserSteps


#! complete this section
@Client.on_message(filters.regex(messages.Messages.BACK.value))
async def back_nav(client, message):
  step = usercache.get_last_step(message.from_user.id)
  parent = uxhandler.UXTree.nodes[step].parent
  if step != UserSteps.START.value:
    await message.reply(text=parent.description, reply_markup=parent.keyboard)
    user_db.update_user_step(message.from_user.id, parent.step)
