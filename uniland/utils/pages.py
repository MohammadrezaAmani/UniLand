from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

from uniland.utils.enums import DocType
from uniland.utils.triggers import Triggers


class Pages:
    """
    A class that defines different keyboard layouts for different pages in the application.

    Attributes:
        HOME: ReplyKeyboardMarkup - Keyboard layout for the home page.
        ADMIN_HOME: ReplyKeyboardMarkup - Keyboard layout for the admin home page.
        ADMIN_PANEL: ReplyKeyboardMarkup - Keyboard layout for the admin panel page.
        ADMIN_PANEL_CHOOSE_NEW_ACCESS_LEVEL: ReplyKeyboardMarkup - Keyboard layout for choosing a new access level in the admin panel.
        EDITOR_PANEL: ReplyKeyboardMarkup - Keyboard layout for the editor panel page.
        BACK: ReplyKeyboardMarkup - Keyboard layout for the back button.
        EMPTY: ReplyKeyboardMarkup - Keyboard layout for an empty keyboard.
        CHOOSE_SUBMISSION_TYPE: ReplyKeyboardMarkup - Keyboard layout for choosing a submission type.
        DOCUMENT_SUBMISSION: ReplyKeyboardMarkup - Keyboard layout for the document submission page.
        DOCUMENT_SUBMISSION_FILE_TYPE: ReplyKeyboardMarkup - Keyboard layout for choosing a file type in the document submission page.
        PROFILE_SUBMISSION: ReplyKeyboardMarkup - Keyboard layout for the profile submission page.
        EDIT_PROFILE_SUBMISSION_PHOTO: ReplyKeyboardMarkup - Keyboard layout for editing the profile submission photo.
        MEDIA_SUBMISSION: InlineKeyboardMarkup - Keyboard layout for the media submission page.
        EDIT_DOCUMENT_SUBMISSION: ReplyKeyboardMarkup - Keyboard layout for editing the document submission page.
        EDIT_DOCUMENT_SUBMISSION_REMOVE_CAUTION: ReplyKeyboardMarkup - Keyboard layout for the caution message when removing a document submission.
        EDIT_PROFILE_SUBMISSION: ReplyKeyboardMarkup - Keyboard layout for editing the profile submission page.
        EDIT_PROFILE_SUBMISSION_REMOVE_CAUTION: ReplyKeyboardMarkup - Keyboard layout for the caution message when removing a profile submission.
    """

    HOME = ReplyKeyboardMarkup(
        [
            [Triggers.SEARCH.value, Triggers.CHOOSE_SUBMISSION_TYPE.value],
            [Triggers.HELP.value, Triggers.MY_PROFILE.value],
        ],
        resize_keyboard=True,
    )
    ADMIN_HOME = ReplyKeyboardMarkup(
        [
            [Triggers.SEARCH.value, Triggers.CHOOSE_SUBMISSION_TYPE.value],
            [Triggers.HELP.value, Triggers.MY_PROFILE.value],
            [Triggers.ADMIN_PANEL.value],
        ],
        resize_keyboard=True,
    )

    ADMIN_PANEL = ReplyKeyboardMarkup(
        [
            [Triggers.GET_SUBMISSION_TO_APPROVE.value],
            [Triggers.UPDATE_USER_ACCESS.value],
            [Triggers.EDIT_SUBMISSION.value],
            [Triggers.BACK.value],
        ],
        resize_keyboard=True,
    )

    ADMIN_PANEL_CHOOSE_NEW_ACCESS_LEVEL = ReplyKeyboardMarkup(
        [
            [
                Triggers.USER_ACCESS_LEVEL_ADMIN.value,
                Triggers.USER_ACCESS_LEVEL_EDITOR.value,
                Triggers.USER_ACCESS_LEVEL_BASIC.value,
            ],
            [Triggers.BACK.value],
        ],
        resize_keyboard=True,
    )

    EDITOR_PANEL = ReplyKeyboardMarkup(
        [
            [Triggers.GET_SUBMISSION_TO_APPROVE.value],
            [Triggers.EDIT_SUBMISSION.value],
            [Triggers.BACK.value],
        ],
        resize_keyboard=True,
    )

    BACK = ReplyKeyboardMarkup([[Triggers.BACK.value]], resize_keyboard=True)
    EMPTY = ReplyKeyboardMarkup(
        [],
        resize_keyboard=True,
    )

    CHOOSE_SUBMISSION_TYPE = ReplyKeyboardMarkup(
        [
            [Triggers.DOCUMENT_SUBMISSION_FILE.value],
            [Triggers.PROFILE_SUBMISSION_INPUT_TITLE.value],
            # [Triggers.MEDIA_SUBMISSION.value],
            [Triggers.BACK.value],
        ],
        resize_keyboard=True,
    )

    DOCUMENT_SUBMISSION = ReplyKeyboardMarkup(
        [
            [
                Triggers.DOCUMENT_SUBMISSION_FILE_TYPE.value,
                Triggers.DOCUMENT_SUBMISSION_COURSE.value,
                Triggers.DOCUMENT_SUBMISSION_PROFESSOR.value,
            ],
            [
                Triggers.DOCUMENT_SUBMISSION_FACULTY.value,
                Triggers.DOCUMENT_SUBMISSION_UNIVERSITY.value,
                Triggers.DOCUMENT_SUBMISSION_WRITER.value,
            ],
            [
                Triggers.DOCUMENT_SUBMISSION_OWNER_TITLE.value,
                Triggers.DOCUMENT_SUBMISSION_SEMESTER_YEAR.value,
                Triggers.DOCUMENT_SUBMISSION_DESCRIPTION.value,
            ],
            [
                Triggers.DOCUMENT_SUBMISSION_DONE.value,
                Triggers.DOCUMENT_SUBMISSION_CANCEL.value,
            ],
        ],
        resize_keyboard=True,
    )

    DOCUMENT_SUBMISSION_FILE_TYPE = ReplyKeyboardMarkup(
        [
            [DocType.BOOK.value, DocType.Pamphlet.value],
            [DocType.Exercises.value, DocType.Template.value],
            [DocType.CompressedFile.value],
            [Triggers.BACK.value],
        ],
        resize_keyboard=True,
    )

    PROFILE_SUBMISSION = ReplyKeyboardMarkup(
        [
            [
                Triggers.PROFILE_SUBMISSION_EMAIL.value,
                Triggers.PROFILE_SUBMISSION_PHONE.value,
                Triggers.PROFILE_SUBMISSION_EDIT_TITLE.value,
            ],
            [
                Triggers.PROFILE_SUBMISSION_FACULTY.value,
                Triggers.PROFILE_SUBMISSION_UNIVERSITY.value,
                Triggers.PROFILE_SUBMISSION_PHOTO.value,
            ],
            [
                Triggers.PROFILE_SUBMISSION_DESCRIPTION.value,
                Triggers.PROFILE_SUBMISSION_OWNER_TITLE.value,
            ],
            [
                Triggers.DOCUMENT_SUBMISSION_DONE.value,
                Triggers.DOCUMENT_SUBMISSION_CANCEL.value,
            ],
        ],
        resize_keyboard=True,
    )

    EDIT_PROFILE_SUBMISSION_PHOTO = ReplyKeyboardMarkup(
        [[Triggers.PROFILE_SUBMISSION_DELETE_PHOTO.value], [Triggers.BACK.value]],
        resize_keyboard=True,
    )

    MEDIA_SUBMISSION = InlineKeyboardMarkup(
        [
            IKB(text="📂 Select File", switch_inline_query_current_chat=""),
        ]
    )

    EDIT_DOCUMENT_SUBMISSION = ReplyKeyboardMarkup(
        [
            [
                Triggers.DOCUMENT_SUBMISSION_FILE_TYPE.value,
                Triggers.DOCUMENT_SUBMISSION_COURSE.value,
                Triggers.DOCUMENT_SUBMISSION_PROFESSOR.value,
            ],
            [
                Triggers.DOCUMENT_SUBMISSION_FACULTY.value,
                Triggers.DOCUMENT_SUBMISSION_UNIVERSITY.value,
                Triggers.DOCUMENT_SUBMISSION_WRITER.value,
            ],
            [
                Triggers.DOCUMENT_SUBMISSION_OWNER_TITLE.value,
                Triggers.DOCUMENT_SUBMISSION_SEMESTER_YEAR.value,
                Triggers.DOCUMENT_SUBMISSION_DESCRIPTION.value,
            ],
            [
                Triggers.DOCUMENT_SUBMISSION_DONE.value,
                Triggers.EDIT_DOCUMENT_SUBMISSION_REMOVE_CAUTION.value,
                Triggers.DOCUMENT_SUBMISSION_CANCEL.value,
            ],
        ],
        resize_keyboard=True,
    )

    EDIT_DOCUMENT_SUBMISSION_REMOVE_CAUTION = ReplyKeyboardMarkup(
        [[Triggers.EDIT_DOCUMENT_SUBMISSION_REMOVE.value], [Triggers.BACK.value]],
        resize_keyboard=True,
    )

    EDIT_PROFILE_SUBMISSION = ReplyKeyboardMarkup(
        [
            [
                Triggers.PROFILE_SUBMISSION_EMAIL.value,
                Triggers.PROFILE_SUBMISSION_PHONE.value,
                Triggers.PROFILE_SUBMISSION_EDIT_TITLE.value,
            ],
            [
                Triggers.PROFILE_SUBMISSION_FACULTY.value,
                Triggers.PROFILE_SUBMISSION_UNIVERSITY.value,
                Triggers.PROFILE_SUBMISSION_PHOTO.value,
            ],
            [
                Triggers.PROFILE_SUBMISSION_DESCRIPTION.value,
                Triggers.PROFILE_SUBMISSION_OWNER_TITLE.value,
            ],
            [
                Triggers.DOCUMENT_SUBMISSION_DONE.value,
                Triggers.EDIT_DOCUMENT_SUBMISSION_REMOVE_CAUTION.value,
                Triggers.DOCUMENT_SUBMISSION_CANCEL.value,
            ],
        ],
        resize_keyboard=True,
    )

    EDIT_PROFILE_SUBMISSION_REMOVE_CAUTION = ReplyKeyboardMarkup(
        [[Triggers.EDIT_PROFILE_SUBMISSION_REMOVE.value], [Triggers.BACK.value]],
        resize_keyboard=True,
    )
