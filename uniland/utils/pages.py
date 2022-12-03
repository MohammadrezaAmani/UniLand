import enum
from uniland.utils.messages import Messages

from pyrogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from pyrogram.types import (
    ReplyKeyboardMarkup as RKM,
    InlineKeyboardMarkup as IKM,
    InlineKeyboardButton as IKB,
    InlineQueryResultArticle as IQRA,
    InputTextMessageContent as ITMC,
)


class Pages:
    HOME = ReplyKeyboardMarkup(
        [
            [Messages.MY_BOOKMARKS.value, Messages.SUBMIT.value],
            [Messages.SEARCH.value, Messages.MY_PROFILE.value],
            [Messages.HELP.value, Messages.ABOUT_US.value],
        ],
        resize_keyboard=True,
    )
    BACK = ReplyKeyboardMarkup([[Messages.BACK.value]], resize_keyboard=True)
    EMPTY = ReplyKeyboardMarkup(
        [],
        resize_keyboard=True,
    )
    SUBMIT = ReplyKeyboardMarkup(
        [
            [Messages.DOCUMENT.value, Messages.PROFILE.value, Messages.MEDIA.value],
            [Messages.BACK.value],
        ],
        resize_keyboard=True,
    )
    DOCUMENT_SUBMISSION = InlineKeyboardMarkup(
        [
            [
                IKB(
                    text=Messages.DOCUMENT_SUBMISSION.value,
                    switch_inline_query_current_chat="",
                )
            ],
            [IKB(text=Messages.BACK.value, switch_inline_query_current_chat="")],
            [
                IKB(
                    text=Messages.DOCUMENT_TYPE.value,
                    switch_inline_query_current_chat="",
                )
            ],
            [
                IKB(
                    text=Messages.UNIVERSITY.value, switch_inline_query_current_chat=""
                ),
                IKB(text=Messages.FACULTY.value, switch_inline_query_current_chat=""),
            ],
            [IKB(text=Messages.COURSE_NAME.value, switch_inline_query_current_chat="")],
            [
                IKB(text=Messages.MASTER.value, switch_inline_query_current_chat=""),
                IKB(text=Messages.YEAR.value, switch_inline_query_current_chat=""),
                IKB(text=Messages.WRITER.value, switch_inline_query_current_chat=""),
            ],
            [
                IKB(text=Messages.FINISH.value, switch_inline_query_current_chat=""),
                IKB(text=Messages.BACK.value, switch_inline_query_current_chat=""),
            ],
            #     [
            #         IKB(
            #             text=Messages.BACK.value, switch_inline_query_current_chat=""
            #         ),IKB(
            #             text=Messages.DOCUMENT_TYPE.value, switch_inline_query_current_chat=""
            #         ),
            #     ],
            #     [
            #         IKB(
            #             text=Messages.UNIVERSITY.value, switch_inline_query_current_chat=""
            #         ),
            #         IKB()
        ]
    )
    PROFILE_SUBMISSION = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="📂 Select File", switch_inline_query_current_chat=""
                ),
            ]
        ]
    )
    MEDIA_SUBMISSION = InlineKeyboardMarkup(
        [
            IKB(text="📂 Select File", switch_inline_query_current_chat=""),
        ]
    )
