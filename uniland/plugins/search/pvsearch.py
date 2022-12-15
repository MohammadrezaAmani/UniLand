from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.enums import ParseMode
from uniland import search_engine, usercache
from uniland.utils.triggers import Triggers
import uniland.db.user_methods as user_db
import uniland.db.submission_methods as sub_db
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree
from uniland.utils.filters import user_step, exact_match
from uniland.plugins.start.start import start_stage
from uniland.utils.builders import Builder


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
    await message.reply(text='.متن جستجو بیش از حد طولانی است')
    return

  search_text = message.text.replace(':', ' ')

  results = [
      Builder.get_submission_child(record.id, record.type)
      for record in search_engine.search(search_text)
  ]

  page, page_size = 0, 5
  display_text, buttons = Builder.get_navigation(
      results[page * page_size:min((page + 1) *
                                   page_size, len(results))], page,
      page_size, f'🌐 نتایج جستجو برای {search_text}\n\n',
      lambda sub: f'{sub.user_display()}\n',
      lambda page, page_size: f'pvsearch:{page}:{page_size}:{search_text}')

  await message.reply(text=display_text,
                      reply_markup=InlineKeyboardMarkup(buttons),
                      parse_mode=ParseMode.DISABLED)
  new_step = UXTree.nodes[UserSteps.SEARCH.value].parent
  await start_stage(client, message)


@Client.on_callback_query(filters.regex('^pvsearch:'))
async def pvsearch_callback(client, callback_query):
  page, page_size, search_text = callback_query.data.split(':')[1:]
  page, page_size = int(page), int(page_size)

  if page < 0:
    await callback_query.answer(text='.این صفحه اول است', show_alert=True)
    return

  results = [
      Builder.get_submission_child(record.id, record.type)
      for record in search_engine.search(search_text)
  ]

  if len(results) <= page * page_size:
    await callback_query.answer(text='.این صفحه آخر است', show_alert=True)
    return

  display_text, buttons = Builder.get_navigation(
      results[page * page_size:min((page + 1) *
                                   page_size, len(results))], page,
      page_size, f'نتایج جستجو برای {search_text}\n\n',
      lambda sub: f'{sub.user_display()}\n',
      lambda page, page_size: f'pvsearch:{page}:{page_size}:{search_text}')

  await callback_query.edit_message_text(
      display_text,
      reply_markup=InlineKeyboardMarkup(buttons),
      parse_mode=ParseMode.DISABLED)


@Client.on_message(filters.text & filters.regex('^/get_'))
async def get_submission(client, message):
  submission_type, submission_id = message.text.split('_')[1:]
  submission = Builder.get_submission_child(submission_id, submission_type)
  if submission == None or not submission.is_confirmed:
    await message.reply(text='.این رکورد وجود ندارد')
    return

  file_id, caption, keyboard = Builder.file_message_generator(submission)
  if not keyboard:
    await message.reply(text='.این رکورد وجود ندارد')
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

  try:
    if not usercache.has_user(message.from_user.id):
      user_db.add_user(message.from_user.id, last_step=UserSteps.START.value)
  except:
    print('None user found in pvsearch')

  sub_db.increase_search_times(id=submission.id)
