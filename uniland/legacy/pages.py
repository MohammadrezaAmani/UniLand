from uniland.utils import triggers
from pyrogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

HOME = ReplyKeyboardMarkup(
    [
        [triggers.DOCUMENT_TITLE, triggers.SOURCE],
        [triggers.RECORDED_CLASSES, triggers.MY_PROFILE],
        [triggers.HELP, triggers.ERTEBAT],  # Second row
    ],
    resize_keyboard=True,
)
BACK = ReplyKeyboardMarkup([[triggers.BACK]], resize_keyboard=True)

EMPTY = ReplyKeyboardMarkup(
    [],
    resize_keyboard=True,
)
CONFIRM_OR_BACK = ReplyKeyboardMarkup(
    [[triggers.BACK, triggers.CONFIRM]], resize_keyboard=True
)
DOCUMENT = ReplyKeyboardMarkup(
    [
        [triggers.DOCUMENT_SEARCH, triggers.DOCUMENT_SUBMISSION],
        [triggers.DOCUMENT_REQUESTED, triggers.BACK],
    ],
    resize_keyboard=True,
)

DOCUMENT_SUBMISSION = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                triggers.DOCUMENT_SUBMISSION_NO,
                callback_data=triggers.DOCUMENT_SUBMISSION_NO + ":document",
            )
        ],
        [
            InlineKeyboardButton(
                triggers.DOCUMENT_SUBMISSION_FACULTY,
                callback_data=triggers.DOCUMENT_SUBMISSION_FACULTY + ":document",
            ),
            InlineKeyboardButton(
                triggers.DOCUMENT_SUBMISSION_NAME,
                callback_data=triggers.DOCUMENT_SUBMISSION_NAME + ":document",
            ),
        ],
        [
            InlineKeyboardButton(
                triggers.DOCUMENT_SUBMISSION_FACULTY,
                callback_data=triggers.DOCUMENT_SUBMISSION_PROFESSOR + ":document",
            ),
            InlineKeyboardButton(
                triggers.DOCUMENT_SUBMISSION_YEAR,
                callback_data=triggers.DOCUMENT_SUBMISSION_YEAR + ":document",
            ),
            InlineKeyboardButton(
                triggers.DOCUMENT_SUBMISSION_WRITER,
                callback_data=triggers.DOCUMENT_SUBMISSION_WRITER + ":document",
            ),
        ],
        [
            InlineKeyboardButton(
                triggers.DOCUMENT_SUBMISSION_CONFIRM,
                callback_data=triggers.DOCUMENT_SUBMISSION_CONFIRM + ":document",
            )
        ],
    ]
)
DOCUMENT_SUBMISSION_NO = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                triggers.DOCUMENT_SUBMISSION_NO_DOCUMENT,
                callback_data=triggers.DOCUMENT_SUBMISSION_NO_DOCUMENT + ":document",
            ),
            InlineKeyboardButton(
                triggers.DOCUMENT_SUBMISSION_NO_NEMONE_SOAL,
                callback_data=triggers.DOCUMENT_SUBMISSION_NO_NEMONE_SOAL + ":document",
            ),
            InlineKeyboardButton(
                triggers.DOCUMENT_SUBMISSION_NO_KHOLASE,
                callback_data=triggers.DOCUMENT_SUBMISSION_NO_KHOLASE + ":document",
            ),
        ],
    ]
)


def YEAR_CREATOR(use: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    triggers.YEARS[i + 3 * j],
                    callback_data=triggers.YEARS[i + 3 * j] + use,
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
                    triggers.FACULTIES[i + 4 * j],
                    callback_data=triggers.FACULTIES[i + 4 * j] + use,
                )
                for i in range(4)
            ]
            for j in range(5)
        ]
    )


DOCUMENT_YEAR = YEAR_CREATOR(triggers.DOCUMENT_TITLE)
DOCUMENT_FACULTY = FACULITY_CREATOR(triggers.DOCUMENT_TITLE)

SOURCE = ReplyKeyboardMarkup(
    [
        [triggers.SOURCE_SEARCH, triggers.SOURCE_SUBMISSION],
        [triggers.SOURCE_REQUESTED, triggers.BACK],
    ],
    resize_keyboard=True,
)

RECORDED = ReplyKeyboardMarkup(
    [
        [triggers.RECORDED_SEARCH, triggers.RECORDED_SUBMISSION],
        [triggers.RECORDED_REQUESTED, triggers.BACK],
    ],
    resize_keyboard=True,
)

PROFILE = ReplyKeyboardMarkup(
    [
        [triggers.MY_SETTINGS, triggers.MY_EMTIYAZ],
        [
            triggers.BACK,
        ],
    ],
    resize_keyboard=True,
)


def LIKE_OR_DISLIKE(part: str, id: int, likes: int, dislikes: int):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    str(likes) + " " + triggers.LIKE,
                    callback_data="like" + ":" + part + ":" + str(id),
                ),
                InlineKeyboardButton(
                    str(dislikes) + " " + triggers.DISLIKE,
                    callback_data="dislike" + ":" + part + ":" + str(id),
                ),
            ],
        ]
    )
