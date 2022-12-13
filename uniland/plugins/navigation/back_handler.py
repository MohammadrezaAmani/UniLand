from pyrogram import Client, filters
import pyrogram
from uniland.utils import triggers, uxhandler
from uniland import usercache
import uniland.db.user_methods as user_db
from uniland.utils.steps import UserSteps
from uniland.utils.pages import Pages
from uniland.plugins.start.start import start_stage


@Client.on_message(filters.regex(triggers.Triggers.BACK.value))
async def back_nav(client, message):
  step = usercache.get_last_step(message.from_user.id)
  user_step = uxhandler.UXTree.nodes[step]
  if step == UserSteps.START.value:
    return
  if user_step.parent.step == UserSteps.START.value:
    await start_stage(client, message)
  else:
    await message.reply(text=user_step.parent.description, reply_markup=user_step.parent.keyboard)
    user_db.update_user_step(message.from_user.id, user_step.parent.step)

#TODO handle editor vs admin panel
