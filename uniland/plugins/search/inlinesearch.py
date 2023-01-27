# Implementing functionality of bot's inline search

from pyrogram import Client, filters
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton,
                            InlineQueryResultCachedDocument)

from uniland import search_engine, usercache
from uniland.db import user_methods as user_db
from uniland.db import doc_methods as doc_db
from uniland.db import profile_methods as profile_db
from uniland.db import media_methods as media_db
from uniland.db import submission_methods as sub_db
from uniland.plugins.dashboard.help import get_keyboard
from uniland.utils.messages import Messages
from uniland.utils.steps import UserSteps
from uniland.config import SEARCH_BACKDOOR_GROUP


@Client.on_inline_query(~filters.bot)
async def answer(client, inline_query):
  ignored, records = search_engine.search(inline_query.query)

  if len(records) > 50:
    records = records[:50]

  results = []
  for record in records:
    # ---------------------- Document ----------------------
    if record.type == 'document':
      document = doc_db.get_document(record.id)
      if document == None:
        continue
      results.append(
        InlineQueryResultCachedDocument(
          document_file_id=document.file_id,
          title=record.search_text,
          id=record.id,
          caption=document.user_display() + '\n' + "آیدی ربات: @UniLandBot",
          description=f'{record.likes} پسند | {document.description}',
          reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
              text=f'👍 {record.likes}',
              callback_data=f"bookmark:{record.id}:{record.likes}")
          ]])))
    # ---------------------- Profile ----------------------
    elif record.type == 'profile':
      profile = profile_db.get_profile(record.id)
      if profile == None:
        continue
      # ------------- Profile with Photo -------------
      if profile.image_id != None and profile.image_id != '':
        results.append(
          InlineQueryResultCachedDocument(
            document_file_id=profile.image_id,
            title=record.search_text,
            id=record.id,
            caption=profile.user_display() + '\n' + "آیدی ربات: @UniLandBot",
            description=f'{record.likes} پسند | {profile.description}',
            reply_markup=InlineKeyboardMarkup([[
              InlineKeyboardButton(
                text=f'👍 {record.likes}',
                callback_data=f"bookmark:{record.id}:{record.likes}")
            ]])))
      # ------------- Profile without Photo -------------
      else:
        results.append(
          InlineQueryResultArticle(
            title=record.search_text,
            input_message_content=InputTextMessageContent(
              profile.user_display() + '\n' + "آیدی ربات: @UniLandBot"),
            id=record.id,
            description=f'{record.likes} پسند | {profile.description}',
            reply_markup=InlineKeyboardMarkup([[
              InlineKeyboardButton(
                text=f'👍 {record.likes}',
                callback_data=f"bookmark:{record.id}:{record.likes}")
            ]])))
    # ---------------------- Media ----------------------
    elif record.type == 'media':
      media = media_db.get_media(record.id)
      if media == None:
        continue
      results.append(
        InlineQueryResultArticle(
          title=record.search_text,
          input_message_content=InputTextMessageContent(
            media.user_display() + '\n' + "آیدی ربات: @UniLandBot"),
          id=record.id,
          description=f'{record.likes} پسند | {media.description}',
          reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton(
              text=f'👍 {media.likes}',
              callback_data=f"bookmark:{record.id}:{record.likes}")
          ]])))

  if len(results) == 0:
    results.append(
      InlineQueryResultArticle(title='راهنما',
                               description='.موردی برای نمایش یافت نشد',
                               input_message_content=InputTextMessageContent(
                                 Messages.HELP_MENU_SEARCH.value),
                               id=-1,
                               reply_markup=InlineKeyboardMarkup(
                                 get_keyboard(1))))

  await inline_query.answer(results=results, cache_time=1)
  # TODO! Remove this part...
  try:
    if len(inline_query.query) > 3 and ignored:
      await client.send_message(
          chat_id=SEARCH_BACKDOOR_GROUP,
        text=
        f'{inline_query.query.strip()}\n\n From {inline_query.from_user.first_name}'
      )
  except Exception as e:
    print(e)


@Client.on_chosen_inline_result()
async def update_search_stats(client, chosen_inline_result):
  if not usercache.has_user(chosen_inline_result.from_user.id):
    user_db.add_user(chosen_inline_result.from_user.id,
                     last_step=UserSteps.START.value)

  if chosen_inline_result.result_id != '-1':
    sub_db.increase_search_times(id=int(chosen_inline_result.result_id))


@Client.on_callback_query(filters.regex('^bookmark:'))
async def toggle_user_bookmark(client, callback_query):
  if not usercache.has_user(callback_query.from_user.id):
    user_db.add_user(callback_query.from_user.id,
                     last_step=UserSteps.START.value)

  _, sub_id, likes = callback_query.data.split(':')
  sub_id, likes = int(sub_id), int(likes)
  
  if not sub_id in search_engine.subs:
    await callback_query.answer('این محتوا حذف شده است.')
    return

  result, new_likes = user_db.toggle_bookmark(callback_query.from_user.id,
                                              sub_id)

  if result == 0:
    await callback_query.answer('Something Went Wrong!')
    return
  elif result == 1:
    await callback_query.answer('به پسندها اضافه شد.')
  else:
    await callback_query.answer('از پسندها حذف شد.')

  if new_likes != likes:
    await callback_query.edit_message_reply_markup(
      InlineKeyboardMarkup([[
        InlineKeyboardButton(text=f'👍 {new_likes}',
                             callback_data=f"bookmark:{sub_id}:{new_likes}")
      ]]))
