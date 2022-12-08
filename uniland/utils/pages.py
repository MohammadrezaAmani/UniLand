import enum
from uniland.utils.triggers import Triggers
from uniland.utils.enums import DocType
# from uniland.db.doc_methods import get_document
# from uniland.db.profile_methods import get_profile
# from uniland.db.media_methods import get_media

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
          [Triggers.MY_BOOKMARKS.value, Triggers.CHOOSE_SUBMISSION_TYPE.value],
          [Triggers.SEARCH.value, Triggers.MY_PROFILE.value],
          [Triggers.HELP.value],
      ],
      resize_keyboard=True,
  )
  ADMIN_HOME = ReplyKeyboardMarkup(
      [
          [Triggers.MY_BOOKMARKS.value, Triggers.CHOOSE_SUBMISSION_TYPE.value],
          [Triggers.SEARCH.value, Triggers.MY_PROFILE.value],
          [Triggers.HELP.value, Triggers.ADMIN_PANEL.value],
      ],
      resize_keyboard=True,
  )

  ADMIN_PANEL = ReplyKeyboardMarkup(
      [[Triggers.GET_SUBMISSION_TO_APPROVE.value],
       [Triggers.UPDATE_USER_ACCESS.value],
          [Triggers.ADMIN_EDIT_SUBMISSIONS.value],
          [Triggers.BACK.value]],
      resize_keyboard=True)

  BACK = ReplyKeyboardMarkup([[Triggers.BACK.value]], resize_keyboard=True)
  EMPTY = ReplyKeyboardMarkup(
      [],
      resize_keyboard=True,
  )
  CHOOSE_SUBMISSION_TYPE = ReplyKeyboardMarkup([
      [Triggers.DOCUMENT_SUBMISSION_FILE.value],
      [Triggers.PROFILE_SUBMISSION_INPUT_TITLE.value],
      [Triggers.MEDIA_SUBMISSION.value],
      [Triggers.BACK.value],
  ],
      resize_keyboard=True)

  DOCUMENT_SUBMISSION = ReplyKeyboardMarkup(
      [[
          Triggers.DOCUMENT_SUBMISSION_FILE_TYPE.value,
          Triggers.DOCUMENT_SUBMISSION_COURSE.value,
          Triggers.DOCUMENT_SUBMISSION_PROFESSOR.value
      ],
          [
          Triggers.DOCUMENT_SUBMISSION_UNIVERSITY.value,
          Triggers.DOCUMENT_SUBMISSION_FACULTY.value,
          Triggers.DOCUMENT_SUBMISSION_SEMESTER_YEAR.value
      ],
          [
          Triggers.DOCUMENT_SUBMISSION_WRITER.value,
          Triggers.DOCUMENT_SUBMISSION_OWNER_TITLE.value,
          Triggers.DOCUMENT_SUBMISSION_DESCRIPTION.value
      ],
          [
          Triggers.DOCUMENT_SUBMISSION_DONE.value,
          Triggers.DOCUMENT_SUBMISSION_CANCEL.value
      ]],
      resize_keyboard=True)

  DOCUMENT_SUBMISSION_FILE_TYPE = ReplyKeyboardMarkup(
      [[DocType.BOOK.value, DocType.Pamphlet.value],
       [DocType.Exercises.value, DocType.CompressedFile.value],
          [Triggers.BACK.value]
       ])

  PROFILE_SUBMISSION = ReplyKeyboardMarkup(
      [[
          Triggers.PROFILE_SUBMISSION_EMAIL.value,
          Triggers.PROFILE_SUBMISSION_PHONE.value,
          Triggers.PROFILE_SUBMISSION_EDIT_TITLE.value
      ],
          [
          Triggers.PROFILE_SUBMISSION_FACULTY.value,
          Triggers.PROFILE_SUBMISSION_UNIVERSITY.value,
          Triggers.PROFILE_SUBMISSION_PHOTO.value
      ],
          [
          Triggers.PROFILE_SUBMISSION_DESCRIPTION.value,
          Triggers.PROFILE_SUBMISSION_OWNER_TITLE.value
      ],
          [
          Triggers.DOCUMENT_SUBMISSION_DONE.value,
          Triggers.DOCUMENT_SUBMISSION_CANCEL.value
      ]],
      resize_keyboard=True)

  EDIT_PROFILE_SUBMISSION_PHOTO = ReplyKeyboardMarkup(
      [[Triggers.PROFILE_SUBMISSION_DELETE_PHOTO.value], [Triggers.BACK.value]],
      resize_keyboard=True)

  MEDIA_SUBMISSION = InlineKeyboardMarkup([
      IKB(text="📂 Select File", switch_inline_query_current_chat=""),
  ])
