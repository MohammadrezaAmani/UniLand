import enum
from uniland.utils.messages import Messages

from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton,InlineQueryResultArticle,
                             InputTextMessageContent)


class Pages(enum.Enum):
  HOME = ReplyKeyboardMarkup(
                [
                    [Messages.MY_BOOKMARKS.value,Messages.SUBMIT.value],
                    [Messages.SEARCH.value,Messages.MY_PROFILE.value],
                    [Messages.HELP.value,Messages.ABOUT_US.value]
                ],
                resize_keyboard=True 
            )
  BACK = ReplyKeyboardMarkup(
                [
                    [Messages.BACK.value]
                ],
                resize_keyboard=True 
            )
  EMPTY = ReplyKeyboardMarkup(
    [],
    resize_keyboard=True,
            )
  SUBMIT = ReplyKeyboardMarkup(
                [
                    [Messages.DOCUMENT.value,Messages.PROFILE.value,Messages.MEDIA],
                  [Messages.BACK]
                ],
                resize_keyboard=True 
            )