from pyrogram import Client, filters
import uniland.db.user_methods as user_db
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree
from uniland.utils.pages import Pages
from uniland import usercache
from uniland.utils.filters import user_exists


@Client.on_message(~user_exists, group=1)
async def handle_new_user(client, message):
  user_db.add_user(message.from_user.id, last_step=UserSteps.START.value)


@Client.on_message(filters.text & filters.command("start") & filters.private)
async def start_stage(client, message):
  user_id = message.from_user.id
  if not usercache.has_user(user_id):
    user_db.add_user(user_id, last_step=UserSteps.START.value)
  start_step = UXTree.nodes[UserSteps.START.value]
  if usercache.has_permission(user_id, min_permission=2, max_permission=3):
    await message.reply(text=start_step.description,
                        reply_markup=Pages.ADMIN_HOME)
  else:
    await message.reply(text=start_step.description,
                        reply_markup=start_step.keyboard)
  user_db.update_user_step(user_id, start_step.step)


# oon chizi k ilya mige
@Client.on_message(group=2)
async def update_last_activity(client, message):
  user_db.update_user_activity(message.from_user.id)
