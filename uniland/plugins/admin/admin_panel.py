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


@Client.on_message(filters.text & user_step(UserSteps.START.value)
                   & exact_match(Triggers.ADMIN_PANEL.value)
                   & access_level(min=3))
async def admin_panel(client, message):
  user_step = UXTree.nodes[UserSteps.ADMIN_PANEL.value]
  output = '🔐 پنل ادمین\n\n'
  output += '📊 آمار ربات:\n'
  output += f'تعداد کل کاربران: {user_db.count_users()}\n'
  output += f'تعداد کل ادمین ها: {user_db.count_admins()}\n'
  output += f'تعداد کل ویرایشگر ها: {user_db.count_editors()}\n'
  output += f'تعداد رکوردها: {sub_db.count_total_submissions()}\n'
  output += f'تعداد رکوردهای تایید شده: {sub_db.count_confirmed_submissions()}\n\n'
  await message.reply(text=output, reply_markup=user_step.keyboard)
  user_db.update_user_step(message.from_user.id, user_step.step)
