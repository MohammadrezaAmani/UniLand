from uniland.utils import messages
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton,InlineQueryResultArticle,
                             InputTextMessageContent)
HOME = ReplyKeyboardMarkup(
                [
                    [messages.JOZVE_TITLE,messages.SOURCE],
                    [messages.RECORDED_CLASSES,messages.MY_PROFILE],
                    [messages.HELP,messages.ERTEBAT]  # Second row
                ],
                resize_keyboard=True 
            )
BACK = ReplyKeyboardMarkup(
                [
                    [messages.BACK]
                ],
                resize_keyboard=True 
            )

EMPTY = ReplyKeyboardMarkup(
    [],
    resize_keyboard=True,

)
CONFIRM_OR_BACK = ReplyKeyboardMarkup(
                [
                    [messages.BACK,messages.CONFIRM]
                ],
                resize_keyboard=True 
            )
JOZVE = ReplyKeyboardMarkup(
                [
                    [messages.JOZVE_SEARCH,messages.JOZVE_SABT],
                    [messages.JOZVE_DARKHASTI,messages.BACK]
                ],
                resize_keyboard=True 
            )

JOZVE_SABT = InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            messages.JOZVE_SABT_NO,
                            callback_data=messages.JOZVE_SABT_NO + messages.JOZVE_TITLE
                        )],
                        [InlineKeyboardButton(
                            messages.JOZVE_SABT_FACULTY,
                            callback_data=messages.JOZVE_SABT_FACULTY + messages.JOZVE_TITLE
                        ), InlineKeyboardButton(
                            messages.JOZVE_SABT_NAME,
                            callback_data=messages.JOZVE_SABT_NAME + messages.JOZVE_TITLE
                        )],[InlineKeyboardButton(
                            messages.JOZVE_SABT_FACULTY,
                            callback_data=messages.JOZVE_SABT_OSTAD + messages.JOZVE_TITLE
                        ), InlineKeyboardButton(
                            messages.JOZVE_SABT_NAME,
                            callback_data=messages.JOZVE_SABT_YEAR + messages.JOZVE_TITLE
                        ), InlineKeyboardButton(
                            messages.JOZVE_SABT_NAME,
                            callback_data=messages.JOZVE_SABT_WRITER + messages.JOZVE_TITLE
                        )],[InlineKeyboardButton(
                            messages.JOZVE_SABT_NAME,
                            callback_data=messages.JOZVE_SABT_CONFIRM + messages.JOZVE_TITLE
                        )],
                    ]
                )
JOZVE_SABT_NO = InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            messages.JOZVE_SABT_NO_JOZVE,
                            callback_data=messages.JOZVE_SABT_NO_JOZVE + messages.JOZVE_TITLE
                        ), InlineKeyboardButton(
                            messages.JOZVE_SABT_NO_NEMONE_SOAL,
                            callback_data=messages.JOZVE_SABT_NO_NEMONE_SOAL + messages.JOZVE_TITLE
                        ), InlineKeyboardButton(
                            messages.JOZVE_SABT_NO_KHOLASE,
                            callback_data=messages.JOZVE_SABT_NO_KHOLASE + messages.JOZVE_TITLE
                        )],
                    ]
)
def YEAR_CREATOR(use:str):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                messages.YEARS[i + 3*j],
                callback_data=messages.YEARS[i + 3*j] + use
                )
     for i in range(3)] for j in range(4)]
    )
def FACULITY_CREATOR(use):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                messages.FACULTIES[i + 4*j],
                callback_data=messages.FACULTIES[i + 4*j] + use
                )
     for i in range(4)] for j in range(5)]
    )
print(messages.FACULTIES)
JOZVE_YEAR = YEAR_CREATOR(messages.JOZVE_TITLE)
JOZVE_FACULTY = FACULITY_CREATOR(messages.JOZVE_TITLE)

SOURCE = ReplyKeyboardMarkup(
                [
                    [messages.SOURCE_SEARCH,messages.SOURCE_SABT],
                    [messages.SOURCE_DARKHASTI,messages.BACK]
                ],
                resize_keyboard=True 
            )

RECORDED = ReplyKeyboardMarkup(
                [
                    [messages.RECORDED_SEARCH,messages.RECORDED_SABT],
                    [messages.RECORDED_DARKHASTI,messages.BACK]
                ],
                resize_keyboard=True 
            )

PROFILE = ReplyKeyboardMarkup(
                [
                    [messages.MY_SETTINGS,messages.MY_EMTIYAZ],
                    [messages.BACK,]
                ],
                resize_keyboard=True 
            )