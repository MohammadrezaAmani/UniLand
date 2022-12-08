from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from uniland import usercache
from uniland.db.tables import User
from uniland.utils.triggers import Triggers
from uniland.utils.messages import Messages
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree
from uniland.db import user_methods as user_db
from uniland.utils.filters import user_step, exact_match
from uniland.utils.builders import Builder
from copy import deepcopy


@Client.on_message(filters.text
                   & user_step(UserSteps.START.value)
                   & exact_match(Triggers.MY_PROFILE.value))
async def show_user_profile(client, message):
    buttons = [
            [
                InlineKeyboardButton(text='نمایش پسندها',
                                    callback_data=f'showbookmarks:{message.from_user.id}:0:5'
                                    )
            ],
            [
                InlineKeyboardButton(text=f'نمایش فایل های من',
                                    callback_data=f'showmysubs:{message.from_user.id}:0:5'
                                    )
            ]
        ]
    
    user_id = message.from_user.id
    score_message = Messages.MYPROFILE_SCORE.value + \
        str(usercache.get_achieved_likes(user_id)) + "\n"
    submitted_message = Messages.SUBMISSIONS_COUNT.value + \
        str(user_db.count_user_submissions(user_id)) + "\n"
    bookmark_message = Messages.BOOKMARKS_TITLE.value + \
        str(user_db.count_user_bookmarks(user_id)) + "\n"
    final_message = score_message + submitted_message + bookmark_message
    await message.reply(text=final_message,
                        reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex('^myprofile'))
async def show_myprofile(client, callback_query):
    buttons = [
        [
            InlineKeyboardButton(text='نمایش پسندها',
                                callback_data=f'showbookmarks:{callback_query.from_user.id}:0:5'
                                )
        ],
        [
            InlineKeyboardButton(text=f'نمایش فایل های من',
                                callback_data=f'showmysubs:{callback_query.from_user.id}:0:5'
                                )
        ]
    ]

    user_id = callback_query.from_user.id
    score_message = Messages.MYPROFILE_SCORE.value + \
        str(usercache.get_achieved_likes(user_id)) + "\n"
    submitted_message = Messages.SUBMISSIONS_COUNT.value + \
        str(user_db.count_user_submissions(user_id)) + "\n"
    bookmark_message = Messages.BOOKMARKS_TITLE.value + \
        str(user_db.count_user_bookmarks(user_id)) + "\n"
    final_message = score_message + submitted_message + bookmark_message
    await callback_query.edit_message_text(text=final_message,
                        reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex('^showbookmarks:'))
async def show_bookmarks_callback(client, callback_query):
  user_id, page, page_size = list(map(int, callback_query.data.split(':')[1:]))

  if page < 0:
    await callback_query.answer(text='این صفحه اول است', show_alert=True)
    return

  results = user_db.get_user_bookmarks(user_id)

  if len(results) <= page * page_size:
    await callback_query.answer(text='این صفحه آخر است', show_alert=True)
    return

  display_text, buttons = Builder.get_navigation(
      results[page * page_size:min((page + 1) *
                                   page_size, len(results))], page,
      page_size, f'پسندهای شما\n\n',
      lambda sub: f'{sub.user_display()}\n',
      lambda page, page_size: f'showbookmarks:{user_id}:{page}:{page_size}')
  
  if not display_text or not buttons:
    await callback_query.answer(text='این صفحه آخر است', show_alert=True)
    return

  buttons.append(
      [InlineKeyboardButton(text='بازگشت به پروفایل من',
                            callback_data='myprofile')]
  )
  
  await callback_query.edit_message_text(
      display_text,
      reply_markup=InlineKeyboardMarkup(buttons),
      parse_mode=ParseMode.DISABLED)


@Client.on_callback_query(filters.regex('^showmysubs:'))
async def show_mysubs_callback(client, callback_query):
  user_id, page, page_size = list(map(int, callback_query.data.split(':')[1:]))

  if page < 0:
    await callback_query.answer(text='این صفحه اول است', show_alert=True)
    return

  results = user_db.get_user_submissions(user_id)

  if len(results) <= page * page_size:
    await callback_query.answer(text='این صفحه آخر است', show_alert=True)
    return

  types = {'document':'فایل', 'profile':'پروفایل', 'media':'رسانه'}

  display_text, buttons = Builder.get_navigation(
      results[page * page_size:min((page + 1) *
                                   page_size, len(results))], page,
      page_size, f'فایل های ثبت شده توسط شما\n\n',
      lambda sub: f"{'✅' if sub.is_confirmed else '❌'} "\
          f"{types[sub.submission_type]}:\n"
          f"{sub.user_display()}\n",
      lambda page, page_size: f'showmysubs:{user_id}:{page}:{page_size}')

  if not display_text or not buttons:
    await callback_query.answer(text='این صفحه آخر است', show_alert=True)
    return

  buttons.append(
      [InlineKeyboardButton(text='بازگشت به پروفایل من', callback_data='myprofile')]
  )

  await callback_query.edit_message_text(
      display_text,
      reply_markup=InlineKeyboardMarkup(buttons),
      parse_mode=ParseMode.DISABLED)

