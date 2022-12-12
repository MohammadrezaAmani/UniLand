from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from uniland import usercache
from uniland.db.tables import User
from uniland.utils.triggers import Triggers
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree
from uniland.utils.filters import user_step, exact_match, access_level
import uniland.db.user_methods as user_db
import uniland.db.submission_methods as sub_db
from uniland.utils.pages import Pages
from uniland.utils.builders import Builder


@Client.on_message(filters.text & user_step(UserSteps.START.value)
                   & exact_match(Triggers.ADMIN_PANEL.value)
                   & access_level(min=2))
async def admin_panel(client, message):
  user_step = UXTree.nodes[UserSteps.ADMIN_PANEL.value]
  text, keyboard = Builder.display_panel(message.from_user.id)
  await message.reply(text, reply_markup=keyboard)
  user_db.update_user_step(message.from_user.id, user_step.step)
