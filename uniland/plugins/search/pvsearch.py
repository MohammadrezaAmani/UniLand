from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from uniland import search_engine
from uniland.utils.triggers import Triggers
import uniland.db.user_methods as user_db
import uniland.db.doc_methods as doc_db
import uniland.db.profile_methods as profile_db
import uniland.db.media_methods as media_db
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree
from uniland.utils.filters import user_step, exact_match
from uniland.plugins.start.start import start_stage


# Builds message components for a submission
def file_message_generator(submission_id, submission_type):
  submission = None
  keyboard = None
  if submission_type == 'document':
    submission = doc_db.get_document(submission_id)
  elif submission_type == 'profile':
    submission = profile_db.get_profile(submission_id)
  elif submission_type == 'media':
    submission = media_db.get_media(submission_id)
  if submission == None:
    return (None, None, None)
  keyboard = InlineKeyboardMarkup([[
      InlineKeyboardButton(
          text=f'👍 {search_engine.get_likes(submission.id)}',
          callback_data=f"bookmark:{submission.id}:{search_engine.get_likes(submission.id)}")
  ]])
  if submission.submission_type == 'document':
    return (submission.file_id, submission.user_display(), keyboard)
  if submission.submission_type == 'profile':
    return (submission.image_id, submission.user_display(), keyboard)


# Builds message components for a page of search results
def get_navigation(search_text: str, page: int, page_size: int):
  buttons = [[
      InlineKeyboardButton(
          text=f'⏮ صفحه قبل',
          callback_data=f"pvsearch:{page-1}:{page_size}:{search_text}"),
      InlineKeyboardButton(
          text=f'صفحه بعد ⏭',
          callback_data=f"pvsearch:{page-1}:{page_size}:{search_text}")
  ]]

  results = search_engine.search(search_text)
  first, last = page * page_size, (page + 1) * page_size
  if first > len(results):
    return None, None, None  # This was last page
  if last > len(results):
    last = len(results)  # Last page is not full
    # buttons.pop(1)
  # if page == 0:
  # buttons.pop(0) # First page doesn't have back button

  first, last = first + 1, last + 1  # For user readability, fixing indices

  # preparing message text
  display_text = f'نتایج جستجو برای "{search_text}"\n\n'
  display_text += f'نتایج {first + 1} تا {last} از {len(results)}\n\n'
  for i, record in enumerate(results[first - 1:last - 1]):
    submission = None
    if record.type == 'document':
      submission = doc_db.get_document(record.id)
    elif record.type == 'profile':
      submission = profile_db.get_profile(record.id)
    elif record.type == 'media':
      submission = media_db.get_media(record.id)

    if submission:
      display_text += f'رکورد {first + i + 1}:\n'
      display_text += submission.user_display() + '\n'
      display_text += f'دریافت رکورد: /get_{submission.submission_type}_{submission.id}\n\n'

  return display_text, buttons


@Client.on_message(filters.text
                   & user_step(UserSteps.START.value)
                   & exact_match(Triggers.SEARCH.value))
async def get_pv_search_text(client, message):
  # Getting search text from user
  user_step = UXTree.nodes[UserSteps.SEARCH.value]
  await message.reply(text=user_step.description,
                      reply_markup=user_step.keyboard)
  user_db.update_user_step(message.from_user.id, user_step.step)


@Client.on_message(filters.text
                   & user_step(UserSteps.SEARCH.value)
                   & ~exact_match(Triggers.BACK.value))
async def display_search_result(client, message):
  if len(message.text) > 100:
    await message.reply(text='متن جستجو بیش از حد طولانی است')
    return
  display_text, buttons = get_navigation(message.text, 0, 5)
  await message.reply(text=display_text,
                      reply_markup=InlineKeyboardMarkup(buttons))
  new_step = UXTree.nodes[UserSteps.SEARCH.value].parent
  await start_stage(client, message)


@Client.on_callback_query(filters.regex('^pvsearch:'))
async def pvsearch_callback(client, callback_query):
  page, page_size, search_text = callback_query.data.split(':')[1:]
  page, page_size = int(page), int(page_size)
  if page < 0:
    await callback_query.answer(text='این صفحه اول است', show_alert=True)
    return
  display_text, buttons = get_navigation(search_text, page, page_size)
  if not display_text:
    await callback_query.answer(text='این صفحه آخر است', show_alert=True)
    return
  await callback_query.edit_message_text(
      display_text, reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_message(filters.text & filters.regex('^/get_'))
async def get_submission(client, message):
  submission_type, submission_id = message.text.split('_')[1:]
  file_id, caption, keyboard = file_message_generator(int(submission_id),
                                                      submission_type)
  if not keyboard:
    await message.reply(text='این رکورد وجود ندارد')
    return

  if submission_type == 'document':
    await message.reply_document(document=file_id,
                                 caption=caption,
                                 reply_markup=keyboard)
  elif submission_type == 'profile':
    if file_id != '':
      await message.reply_document(document=file_id,
                                   caption=caption,
                                   reply_markup=keyboard)
    else:
      await message.reply_text(text=caption, reply_markup=keyboard)
