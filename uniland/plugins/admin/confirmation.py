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
import uniland.db.submission_methods as subs_db
from uniland.utils.pages import Pages
import os
from uniland.utils.builders import Builder


def get_keyboard(submission_id):
  buttons = \
      [
          [
              InlineKeyboardButton(  # accepts
                  "✅ تایید",
                  callback_data="confirmation:accept"
              ),
              InlineKeyboardButton(  # rejects
                  "❌ رد",
                  callback_data="confirmation:reject"
              )
          ],
          [
              InlineKeyboardButton(
                  "✏️ ویرایش",
                  callback_data=f"confirmation:edit:{submission_id}"
              )
          ],
      ]
  return buttons


#TODO better way? / handle multiple requestse
reviewing_subs = {}  # dictionary of submission id to admin id


@Client.on_message(filters.text
                   & user_step(UserSteps.ADMIN_PANEL.value)
                   & exact_match(Triggers.GET_SUBMISSION_TO_APPROVE.value)
                   & access_level(min=2))
async def admin_confirmation(client, message):
  global reviewing_subs
  admin_id = message.from_user.id
  unconfirmed_subs = subs_db.get_unconfirmed_submissions()
  sub_id = 0
  sub = None
  for submission in unconfirmed_subs:
    if submission.id not in reviewing_subs.keys():
      sub_id = submission.id
      sub = subs_db.get_submission(sub_id)
      break
  if sub_id == 0:  # new unconfirmed unreviewed submission not found
    await message.reply(Messages.CONFIRMATION_NO_UNCONFIMRED_FILE.value)
  else:  # found
    reviewing_subs[sub_id] = admin_id
    await message.reply_document(document=sub.file_id,
                                 caption=str(sub),
                                 reply_markup=InlineKeyboardMarkup(
                                     get_keyboard(sub_id)))


@Client.on_callback_query(filters.regex('confirmation:accept'))
async def accept_submission(client, callback_query):
  await callback_query.edit_message_reply_markup([])
  global reviewing_submissions
  earliest_sub.confirm(user_db.get_user(admin_id))

  await callback_query.answer(text="تایید شد. 🍾")


@Client.on_callback_query(filters.regex('confirmation:reject'))
async def reject_submission(client, callback_query):
  await callback_query.edit_message_reply_markup([])
  user_step = UXTree.nodes[UserSteps.GET_REJECTION_REASON.value]
  await callback_query.message.reply(text='علت رد شدن را وارد کنید.',
                                     reply_markup=user_step.keyboard)
  user_db.update_user_step(admin_id, user_step.step)


@Client.on_message(filters.text
                   & user_step(UserSteps.GET_REJECTION_REASON.value)
                   & ~exact_match(Triggers.BACK.value)
                   & access_level(min=2))
async def send_rejection_reason(client, message):
  global earliest_sub
  global earliest_sub_owner_id
  # await message.copy(earliest_sub.owner_id)
  user_step = UXTree.nodes[UserSteps.ADMIN_PANEL.value]
  user_db.update_user_step(admin_id, user_step.step)
  text, keyboard = Builder.display_panel(message.from_user.id)
  await message.reply(text, reply_markup=keyboard)


@Client.on_callback_query(filters.regex("^confirmation:edit"))
async def edit_submission(client, callback_query):
  db_sub_id = int(callback_query.data.split(":")[2])
  submission = subs_db.get_submission(db_sub_id)
  await callback_query.answer("Coming Soon!", show_alert=True)
  #TODO: edit file's description
