import enum
from uniland.utils.messages import Messages
from uniland.utils.enums import DocType

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
            [Messages.MY_BOOKMARKS.value, Messages.CHOOSE_SUBMISSION_TYPE.value],
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
    CHOOSE_SUBMISSION_TYPE = ReplyKeyboardMarkup(
        [
            [Messages.DOCUMENT_SUBMISSION_FILE.value],
            [Messages.PROFILE_SUBMISSION.value],
            [Messages.MEDIA_SUBMISSION.value],
            [Messages.BACK.value],
        ],
        resize_keyboard=True
    )

    DOCUMENT_SUBMISSION = ReplyKeyboardMarkup(
        [
            [
                Messages.DOCUMENT_SUBMISSION_FILE_TYPE.value, 
                Messages.DOCUMENT_SUBMISSION_COURSE.value,
                Messages.DOCUMENT_SUBMISSION_PROFESSOR.value
            ],
            
            [
                Messages.DOCUMENT_SUBMISSION_UNIVERSITY.value,
                Messages.DOCUMENT_SUBMISSION_FACULTY.value,
                Messages.DOCUMENT_SUBMISSION_SEMESTER_YEAR.value
            ],
            
            [
                Messages.DOCUMENT_SUBMISSION_WRITER.value,
                Messages.DOCUMENT_SUBMISSION_OWNER_TITLE.value,
                Messages.DOCUMENT_SUBMISSION_DESCRIPTION.value
            ],
            
            [
                Messages.DOCUMENT_SUBMISSION_DONE.value,
                Messages.DOCUMENT_SUBMISSION_CANCEL.value
            ]
        ],
        resize_keyboard=True
    )
    
    DOCUMENT_SUBMISSION_FILE_TYPE = ReplyKeyboardMarkup(
        [
            [DocType.Pamphlet.value, DocType.Summary.value],
            [DocType.Exercises.value, DocType.ExampleProblems.value],
            [DocType.CompressedFile.value],
            [Messages.BACK.value]
        ]
    )
    
    # Mohmmadreza's previous buttion
    # DOCUMENT_SUBMISSION = InlineKeyboardMarkup(
    #     [
    #         [
    #             IKB(
    #                 text=Messages.DOCUMENT_SUBMISSION.value,
    #                 switch_inline_query_current_chat="",
    #             )
    #         ],
    #         [IKB(text=Messages.BACK.value, switch_inline_query_current_chat="")],
    #         [
    #             IKB(
    #                 text=Messages.DOCUMENT_TYPE.value,
    #                 switch_inline_query_current_chat="",
    #             )
    #         ],
    #         [
    #             IKB(
    #                 text=Messages.UNIVERSITY.value, switch_inline_query_current_chat=""
    #             ),
    #             IKB(text=Messages.FACULTY.value, switch_inline_query_current_chat=""),
    #         ],
    #         [IKB(text=Messages.COURSE_NAME.value, switch_inline_query_current_chat="")],
    #         [
    #             IKB(text=Messages.MASTER.value, switch_inline_query_current_chat=""),
    #             IKB(text=Messages.YEAR.value, switch_inline_query_current_chat=""),
    #             IKB(text=Messages.WRITER.value, switch_inline_query_current_chat=""),
    #         ],
    #         [
    #             IKB(text=Messages.FINISH.value, switch_inline_query_current_chat=""),
    #             IKB(text=Messages.BACK.value, switch_inline_query_current_chat=""),
    #         ],
    #         #     [
    #         #         IKB(
    #         #             text=Messages.BACK.value, switch_inline_query_current_chat=""
    #         #         ),IKB(
    #         #             text=Messages.DOCUMENT_TYPE.value, switch_inline_query_current_chat=""
    #         #         ),
    #         #     ],
    #         #     [
    #         #         IKB(
    #         #             text=Messages.UNIVERSITY.value, switch_inline_query_current_chat=""
    #         #         ),
    #         #         IKB()
    #     ]
    # )
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
