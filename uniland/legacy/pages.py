from uniland.utils import messages
from pyrogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

HOME = ReplyKeyboardMarkup(
    [
        [messages.DOCUMENT_TITLE, messages.SOURCE],
        [messages.RECORDED_CLASSES, messages.MY_PROFILE],
        [messages.HELP, messages.ERTEBAT],  # Second row
    ],
    resize_keyboard=True,
)
BACK = ReplyKeyboardMarkup([[messages.BACK]], resize_keyboard=True)

EMPTY = ReplyKeyboardMarkup(
    [],
    resize_keyboard=True,
)
CONFIRM_OR_BACK = ReplyKeyboardMarkup(
    [[messages.BACK, messages.CONFIRM]], resize_keyboard=True
)
DOCUMENT = ReplyKeyboardMarkup(
    [
        [messages.DOCUMENT_SEARCH, messages.DOCUMENT_SUBMISSION],
        [messages.DOCUMENT_REQUESTED, messages.BACK],
    ],
    resize_keyboard=True,
)

DOCUMENT_SUBMISSION = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                messages.DOCUMENT_SUBMISSION_NO,
                callback_data=messages.DOCUMENT_SUBMISSION_NO + ":document",
            )
        ],
        [
            InlineKeyboardButton(
                messages.DOCUMENT_SUBMISSION_FACULTY,
                callback_data=messages.DOCUMENT_SUBMISSION_FACULTY + ":document",
            ),
            InlineKeyboardButton(
                messages.DOCUMENT_SUBMISSION_NAME,
                callback_data=messages.DOCUMENT_SUBMISSION_NAME + ":document",
            ),
        ],
        [
            InlineKeyboardButton(
                messages.DOCUMENT_SUBMISSION_FACULTY,
                callback_data=messages.DOCUMENT_SUBMISSION_PROFESSOR + ":document",
            ),
            InlineKeyboardButton(
                messages.DOCUMENT_SUBMISSION_YEAR,
                callback_data=messages.DOCUMENT_SUBMISSION_YEAR + ":document",
            ),
            InlineKeyboardButton(
                messages.DOCUMENT_SUBMISSION_WRITER,
                callback_data=messages.DOCUMENT_SUBMISSION_WRITER + ":document",
            ),
        ],
        [
            InlineKeyboardButton(
                messages.DOCUMENT_SUBMISSION_CONFIRM,
                callback_data=messages.DOCUMENT_SUBMISSION_CONFIRM + ":document",
            )
        ],
    ]
)
DOCUMENT_SUBMISSION_NO = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                messages.DOCUMENT_SUBMISSION_NO_DOCUMENT,
                callback_data=messages.DOCUMENT_SUBMISSION_NO_DOCUMENT + ":document",
            ),
            InlineKeyboardButton(
                messages.DOCUMENT_SUBMISSION_NO_NEMONE_SOAL,
                callback_data=messages.DOCUMENT_SUBMISSION_NO_NEMONE_SOAL + ":document",
            ),
            InlineKeyboardButton(
                messages.DOCUMENT_SUBMISSION_NO_KHOLASE,
                callback_data=messages.DOCUMENT_SUBMISSION_NO_KHOLASE + ":document",
            ),
        ],
    ]
)


def YEAR_CREATOR(use: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    messages.YEARS[i + 3 * j],
                    callback_data=messages.YEARS[i + 3 * j] + use,
                )
                for i in range(3)
            ]
            for j in range(4)
        ]
    )


def FACULITY_CREATOR(use):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    messages.FACULTIES[i + 4 * j],
                    callback_data=messages.FACULTIES[i + 4 * j] + use,
                )
                for i in range(4)
            ]
            for j in range(5)
        ]
    )


DOCUMENT_YEAR = YEAR_CREATOR(messages.DOCUMENT_TITLE)
DOCUMENT_FACULTY = FACULITY_CREATOR(messages.DOCUMENT_TITLE)

SOURCE = ReplyKeyboardMarkup(
    [
        [messages.SOURCE_SEARCH, messages.SOURCE_SUBMISSION],
        [messages.SOURCE_REQUESTED, messages.BACK],
    ],
    resize_keyboard=True,
)

RECORDED = ReplyKeyboardMarkup(
    [
        [messages.RECORDED_SEARCH, messages.RECORDED_SUBMISSION],
        [messages.RECORDED_REQUESTED, messages.BACK],
    ],
    resize_keyboard=True,
)

PROFILE = ReplyKeyboardMarkup(
    [
        [messages.MY_SETTINGS, messages.MY_EMTIYAZ],
        [
            messages.BACK,
        ],
    ],
    resize_keyboard=True,
)


def LIKE_OR_DISLIKE(part: str, id: int, likes: int, dislikes: int):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    str(likes) + " " + messages.LIKE,
                    callback_data="like" + ":" + part + ":" + str(id),
                ),
                InlineKeyboardButton(
                    str(dislikes) + " " + messages.DISLIKE,
                    callback_data="dislike" + ":" + part + ":" + str(id),
                ),
            ],
        ]
    )
