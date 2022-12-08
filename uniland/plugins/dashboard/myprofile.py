from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from uniland import usercache
from uniland.db.tables import User
from uniland.utils.triggers import Triggers
from uniland.utils.messages import Messages
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree
from uniland.db import user_methods
from uniland.utils.filters import user_step, exact_match
from copy import deepcopy

buttons = \
    [
        [
            InlineKeyboardButton(  # Shows bookmarks
                Messages.MYPROFILE_BOOKMARKS.value,
                callback_data="MyProfile:display_bookmarks"
            )
        ],
        [
            InlineKeyboardButton(  # Shows submissions
                Messages.MYPROFILE_SUBMISSIONS.value,
                callback_data="MyProfile:display_submissions"
            ),
        ]
    ]


@Client.on_message(filters.text & user_step(UserSteps.START.value)
                   & exact_match(Triggers.MY_PROFILE.value))
async def myprofile_menu(client, message):
    user_id = message.from_user.id
    score_message = Messages.MYPROFILE_SCORE.value + \
        str(usercache.get_achieved_likes(user_id)) + "\n"
    submitted_message = Messages.SUBMISSIONS_COUNT.value + \
        str(user_methods.count_user_submissions(user_id)) + "\n"
    bookmark_message = Messages.BOOKMARKS_TITLE.value + \
        str(user_methods.count_user_bookmarks(user_id)) + "\n"
    final_message = score_message + submitted_message + bookmark_message
    await message.reply(text=final_message,
                        reply_markup=InlineKeyboardMarkup(buttons))


#TODO edit method -> show bookmarks
@Client.on_callback_query(filters.regex('MyProfile:display_bookmarks'))
async def show_bookmarks(client, callback_query):
    await callback_query.edit_message_text("bookmarks")


#TODO edit method -> show submissions
@Client.on_callback_query(filters.regex('MyProfile:display_submissions'))
async def show_submissions(client, callback_query):
    await callback_query.edit_message_text("submissions")
