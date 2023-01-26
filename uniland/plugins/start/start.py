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
async def user_entrance(client, message):
  user_id = message.from_user.id
  if not usercache.has_user(user_id):
    user_db.add_user(user_id, last_step=UserSteps.START.value)

  custom_message = f'سلام {message.from_user.first_name} عزیز'
  custom_message += f'\nبه بات UniLand خوش اومدی!'

  start_step = UXTree.nodes[UserSteps.START.value]
  if usercache.has_permission(user_id, min_permission=2, max_permission=3):
    await message.reply(text=custom_message, reply_markup=Pages.ADMIN_HOME)
  else:
    await message.reply(text=custom_message, reply_markup=start_step.keyboard)
  user_db.update_user_step(user_id, start_step.step)


async def start_stage(client, message):
  user_id = message.from_user.id
  if not usercache.has_user(user_id):
    user_db.add_user(user_id, last_step=UserSteps.START.value)

  custom_message = f'ممنون که همراه مایی {message.from_user.first_name} عزیز، دیگه چه کاری می‌تونم برات انجام بدم؟'

  start_step = UXTree.nodes[UserSteps.START.value]
  if usercache.has_permission(user_id, min_permission=2, max_permission=3):
    await message.reply(text=custom_message, reply_markup=Pages.ADMIN_HOME)
  else:
    await message.reply(text=custom_message, reply_markup=start_step.keyboard)
  user_db.update_user_step(user_id, start_step.step)


@Client.on_message(group=2)
async def update_last_activity_on_message(client, message):
  try:
    if not usercache.has_user(message.from_user.id):
      user_db.add_user(message.from_user.id, last_step=UserSteps.START.value)
    user_db.update_user_activity(message.from_user.id)
  except:
    pass


@Client.on_callback_query(group=2)
async def update_last_activity_on_callback(client, callback_query):
  try:
    if not usercache.has_user(callback_query.from_user.id):
      user_db.add_user(callback_query.from_user.id,
                      last_step=UserSteps.START.value)
    user_db.update_user_activity(callback_query.from_user.id)
  except:
    pass


@Client.on_inline_query(group=2)
async def update_last_activity_on_inline(client, inline_query):
  try:
    if not usercache.has_user(inline_query.from_user.id):
      user_db.add_user(inline_query.from_user.id,
                      last_step=UserSteps.START.value)
    user_db.update_user_activity(inline_query.from_user.id)
  except:
    pass
