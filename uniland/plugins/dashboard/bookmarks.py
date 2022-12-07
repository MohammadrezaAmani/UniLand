from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import uniland.db.user_methods as user_db
from uniland.utils.triggers import Triggers
from uniland.utils.messages import Messages
from uniland.utils.steps import UserSteps
from uniland.utils.filters import user_step, exact_match

# on trigger -> send message(bookmark count)
#               + list(glass button(type:title))
#               + glass button(next page)


def build_keyboard(bookmarks, page=1):

  keyboard = []
  nav_buttons = []
  max_upper = int(len(bookmarks))  # 2
  lower = 10 * (page - 1)  #
  upper = (10 * page) - 1  # 9

  for i in range(lower, upper + 1):  # [0-10)
    if i < max_upper:
      # TODO: imlpement button_text as "FileType:Title"
      button_text = bookmarks[i].search_text
      keyboard.append([
          InlineKeyboardButton(button_text,
                               callback_data=f'bookmarks:subs:{bookmarks[i].id}')
      ])

  if not lower == 0:
    nav_buttons.append(
        InlineKeyboardButton('back', callback_data=f'bookmarks:back:{page-1}'))
  if upper < max_upper:
    nav_buttons.append(
        InlineKeyboardButton('next', callback_data=f'bookmarks:next:{page+1}'))

  if len(nav_buttons) > 0:
    keyboard.append(nav_buttons)
  return InlineKeyboardMarkup(keyboard)


@Client.on_message(filters.text & filters.private
                   & user_step(UserSteps.START.value)
                   & exact_match(Triggers.MY_BOOKMARKS.value))
async def display_bookmarks(client, message):

  bookmarks = user_db.get_user(message.from_user.id).bookmarks

  if bookmarks and len(bookmarks) > 0:
    print(bookmarks)
    #TODO: no bookmarks found text -> messages
    caption_text = Messages.BOOKMARKS_COUNT.value + str(len(bookmarks))
    keyboard = build_keyboard(bookmarks, 1)
    await message.reply(
        text=caption_text,
        reply_markup=keyboard
    )
  else:
    #TODO: no bookmarks found text -> messages
    await message.reply(text='no bookmarks found')


# DONE
@Client.on_callback_query(filters.regex('^(bookmarks:back|bookmarks:next)'))
async def change_pages(client, callback_query):

  bookmarks = user_db.get_user(callback_query.from_user.id).bookmarks

  dst = callback_query.data.split(':')[2]
  await callback_query.edit_message_reply_markup(
      build_keyboard(bookmarks, int(dst)))


@Client.on_callback_query(filters.regex('^bookmarks:subs:'))
async def send_files(client, callback_query):
  file = int(callback_query.data.split(':')[2].id)
  # TODO: send selected file to user


# def build_message(db_file_id) -> (file_id, text, reply_markup:InlineKeyboardMarkup)
#   message(attachment:file_id)
