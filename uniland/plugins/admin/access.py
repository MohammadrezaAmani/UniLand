from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from uniland import usercache
from uniland.db.tables import User
from uniland.utils.triggers import Triggers
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree
from uniland.utils.filters import user_step, exact_match, access_level
import uniland.db.user_methods as user_db
from uniland.utils.pages import Pages
from uniland.utils.messages import Messages
from uniland.utils.enums import UserLevel
from uniland.utils.builders import Builder

user_id_input = {}

@Client.on_message(filters.text
                   & user_step(UserSteps.ADMIN_PANEL.value)
                   & exact_match(Triggers.UPDATE_USER_ACCESS.value)
                   & access_level(min=3))
async def edit_access_level(client, message):
  user_step = UXTree.nodes[UserSteps.UPDATE_USER_ACCESS.value]
  messager_user_id = message.from_user.id
  await message.reply(text=Messages.ACCESS_LEVEL_BY_USERID.value,
                      reply_markup=Pages.BACK)
  user_db.update_user_step(messager_user_id, user_step.step)


@Client.on_message(filters.text
                   & user_step(UserSteps.UPDATE_USER_ACCESS.value)
                   & access_level(min=3)
                   & ~exact_match(Triggers.BACK.value))
async def get_access_level(client, message):
  global user_id_input
  if message.forward_from == None and not message.forward_sender_name == None:
    await message.reply(
      f"شما در حال فوروارد کردن پیامی از {message.forward_sender_name} .هستید. اما قابلیت فوروارد پیام‌ها توسط ایشان بسته شده است."
    )
    return
  elif message.forward_from == None:
    # When message is not forwarded
    user_id_input[message.from_user.id] = message.text
    if not message.text.isnumeric():  # not int
      await message.reply("مقدار وارد شده معتبر نیست. لطفا عدد وارد کنید.")
      return
  else:
    # When message is forwarded
    user_id_input[message.from_user.id] = message.forward_from.id
  # user not in database
  if message.forward_from and not usercache.has_user(int(message.forward_from.id)):
    await message.reply("این یوزر آیدی وجود ندارد. دوباره تلاش کنید.")
    return
  user_step = UXTree.nodes[UserSteps.CHOOSE_USER_ACCESS_LEVEL.value]
  output = Messages.ACCESS_LEVEL_CHOOSE.value
  await message.reply(text=output,
                      reply_markup=Pages.ADMIN_PANEL_CHOOSE_NEW_ACCESS_LEVEL)
  user_db.update_user_step(message.from_user.id, user_step.step)

@Client.on_message(filters.text
                   & user_step(UserSteps.CHOOSE_USER_ACCESS_LEVEL.value)
                   & access_level(min=3)
                   & (exact_match(Triggers.USER_ACCESS_LEVEL_ADMIN.value)
                      | exact_match(Triggers.USER_ACCESS_LEVEL_EDITOR.value)
                      | exact_match(Triggers.USER_ACCESS_LEVEL_BASIC.value)))
async def change_access_level(client, message):
  user_step = UXTree.nodes[UserSteps.ADMIN_PANEL.value]
  global user_id_input
  output = ""
  
  if not message.from_user.id in user_id_input:
    await message.reply_text('خطای گم شدن اطلاعات! لطفا مجددا تلاش نمایید.')
    user_db.update_user_step(message.from_user.id, user_step.step)
    text, keyboard = Builder.display_panel(message.from_user.id)
    await message.reply(text, reply_markup=keyboard)
    return
  
  if not usercache.has_permission(message.from_user.id, min_permission=3):
    await message.reply_text('شما سطح دسترسی مورد نیاز را ندارید!')
    user_db.update_user_step(message.from_user.id, user_step.step)
    text, keyboard = Builder.display_panel(message.from_user.id)
    await message.reply(text, reply_markup=keyboard)
    return

  # convert access level: persian to int
  access_levels_dict = {
    Triggers.USER_ACCESS_LEVEL_ADMIN.value: 3,
    Triggers.USER_ACCESS_LEVEL_EDITOR.value: 2,
    Triggers.USER_ACCESS_LEVEL_BASIC.value: 1,
  }
  new_access_level = access_levels_dict[message.text]
  user_id = int(user_id_input[message.from_user.id])
  user_db.update_user_access_level(user_id,
                                   new_access_level)  # update db & cache
  output = "سطح دسترسی آپدیت شد."
  await message.reply(output)
  user_db.update_user_step(message.from_user.id, user_step.step)
  text, keyboard = Builder.display_panel(message.from_user.id)
  await message.reply(text, reply_markup=keyboard)
