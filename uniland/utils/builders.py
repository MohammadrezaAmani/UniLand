from pyrogram.types import (
  InlineKeyboardMarkup,
  InlineKeyboardButton,
)
from uniland import search_engine
from uniland.db import user_methods as user_db
from uniland.db import doc_methods as doc_db
from uniland.db import profile_methods as profile_db
from uniland.db import media_methods as media_db


class Builder:

  def get_submission_child(submission_id: int, submission_type: str):
    if submission_type == 'document':
      return doc_db.get_document(submission_id)
    elif submission_type == 'profile':
      return profile_db.get_profile(submission_id)
    elif submission_type == 'media':
      return media_db.get_media(submission_id)
    return None

  def file_message_generator(submission):
    if submission == None:
      return (None, None, None)
    keyboard = InlineKeyboardMarkup([[
      InlineKeyboardButton(
        text=f'👍 {search_engine.get_likes(submission.id)}',
        callback_data=
        f"bookmark:{submission.id}:{search_engine.get_likes(submission.id)}")
    ]])
    if submission.submission_type == 'document':
      return (submission.file_id, submission.user_display(), keyboard)
    if submission.submission_type == 'profile':
      return (submission.image_id, submission.user_display(), keyboard)

  def get_navigation(
      submissions: list,
      page: int,
      page_size: int,
      page_title: str,
      text_generator,  # lambda sub
      callback_generator  # lambda sub, page, page_size
  ):

    buttons = [[
      InlineKeyboardButton(text=f'⏮ صفحه قبل',
                           callback_data=callback_generator(
                             page - 1, page_size)),
      InlineKeyboardButton(text=f'صفحه بعد ⏭',
                           callback_data=callback_generator(
                             page + 1, page_size))
    ]]

    first = page * page_size + 1
    last = first + len(submissions) - 1

    # preparing message text
    display_text = page_title
    display_text += f'نتایج {first} تا {last}\n'
    for i, submission in enumerate(submissions):
      if not submission:
        display_text += f'رکورد ناموجود است\n\n'

      else:
        display_text += f'\nرکورد {first + i}:\n'
        display_text += text_generator(submission)
        display_text += f'دریافت رکورد: /get_{submission.submission_type}_{submission.id}\n\n'
        display_text += 20 * '-'

    return display_text, buttons
