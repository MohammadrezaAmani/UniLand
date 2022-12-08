from pyrogram import Client, filters
from uniland import usercache
import uniland.db.user_methods as user_db
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXNode, UXTree
from uniland.utils.pages import Pages
from uniland import usercache


@Client.on_message(filters.text & filters.command("start"))
async def start_stage(client, message):
  user_id = message.from_user.id
  if not usercache.has_user(user_id):
    user_db.add_user(user_id, last_step=UserSteps.START.value)
  start_step = UXTree.nodes[UserSteps.START.value]
  if usercache.has_permission(user_id, min_permission=2, max_permission=3):
    await message.reply(
        text=start_step.description,
        reply_markup=Pages.ADMIN_HOME
    )
  else:
    await message.reply(
        text=start_step.description,
        reply_markup=start_step.keyboard
    )
  user_db.update_user_step(user_id, start_step.step)
