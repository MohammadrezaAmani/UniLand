from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from uniland import usercache
from uniland.db.tables import User
from uniland.utils.triggers import Triggers
from uniland.utils.messages import Messages
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree
from uniland.db import user_methods
from uniland.utils.filters import user_step, exact_match, access_level
from copy import deepcopy
import uniland.db.user_methods as user_db


@Client.on_message(filters.text
                   & user_step(UserSteps.ADMIN_PANEL.value)
                   & exact_match(Triggers.GET_SUBMISSION_TO_APPROVE.value)
                   & access_level(min=3))
async def admin_confirmation(client, message):
  user_step = UXTree.nodes[UserSteps.GET_SUBMISSION_TO_APPROVE.value]
  await message.reply(text="hi there!")
  # user_db.update_user_step(message.from_user.id,
  #                          UserSteps.GET_SUBMISSION_TO_APPROVE.value)
