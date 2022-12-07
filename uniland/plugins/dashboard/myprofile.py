from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from uniland import usercache
from uniland.utils.triggers import Triggers
from uniland.utils.messages import Messages
from uniland.utils.steps import UserSteps
from uniland.utils.uxhandler import UXTree
from uniland.utils.uxhandler import UXTree
from uniland.utils.filters import user_step, exact_match
from copy import deepcopy

buttons = \
    [
        [
            InlineKeyboardButton(  # Opens a web URL
                "نام من",
                callback_data="MyProfile:display_MyName"
            )
        ],
        [
            InlineKeyboardButton(  # Opens a web URL
                "امتیاز من",
                callback_data="MyProfile:display_MyScore"
            ),
        ]
    ]


# TODO: change method name to myprofile menu : Done
@Client.on_message(filters.text & user_step(UserSteps.START.value)
                   & exact_match(Triggers.MY_PROFILE.value))
async def myprofile_menu(client, message):
  score_value = usercache.get_achieved_likes(message.from_user.id)
  score_message = str(score_value) + Messages.MYPROFILE_SCORE.value
  await message.reply(text=score_message,
                      reply_markup=InlineKeyboardMarkup(buttons))


# @Client.on_callback_query(filters.regex('MyProfile:display_MyScore'))
# async def MyScore(client, callback_query):
#     await callback_query.edit_message_text(Messages.MYPROFILE_.value)
#     await callback_query.edit_message_reply_markup(
#         InlineKeyboardMarkup(get_keyboard(3))
#     )
