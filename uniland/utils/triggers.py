import enum


class Triggers(enum.Enum):

    # ----------------- Start -----------------
    START = "/start"
    BACK = "برگشت"

    # ----------------- Search Branch -----------------

    # ----------------- Submit Branch -----------------
    CHOOSE_SUBMISSION_TYPE = "ارسال محتوا"

    DOCUMENT_SUBMISSION_FILE = 'ارسال فایل'
    DOCUMENT_SUBMISSION = "ارسال فایل"
    DOCUMENT_SUBMISSION_CANCEL = '❌ لغو ❌'
    DOCUMENT_SUBMISSION_FILE_TYPE = 'نوع فایل'
    DOCUMENT_SUBMISSION_UNIVERSITY = "دانشگاه"
    DOCUMENT_SUBMISSION_FACULTY = "دانشکده"
    DOCUMENT_SUBMISSION_OWNER_TITLE = "نام ثبت کننده"
    DOCUMENT_SUBMISSION_DESCRIPTION = "توضیحات"
    DOCUMENT_SUBMISSION_COURSE = "نام درس"
    DOCUMENT_SUBMISSION_PROFESSOR = "استاد درس"
    DOCUMENT_SUBMISSION_WRITER = "نویسنده"
    DOCUMENT_SUBMISSION_SEMESTER_YEAR = "سال تهیه"
    DOCUMENT_SUBMISSION_DONE = "✅ اتمام ✅"

    PROFILE_SUBMISSION_INPUT_TITLE = "ارسال اطلاعات"
    PROFILE_SUBMISSION = "ارسال اطلاعات"
    PROFILE_SUBMISSION_CANCEL = '❌ لغو ❌'
    PROFILE_SUBMISSION_EDIT_TITLE = "عنوان"
    PROFILE_SUBMISSION_PHOTO = 'تصویر'
    PROFILE_SUBMISSION_DELETE_PHOTO = 'حذف تصویر فعلی'
    PROFILE_SUBMISSION_UNIVERSITY = "دانشگاه"
    PROFILE_SUBMISSION_FACULTY = "دانشکده"
    PROFILE_SUBMISSION_OWNER_TITLE = "نام ثبت کننده"
    PROFILE_SUBMISSION_DESCRIPTION = "توضیحات"
    PROFILE_SUBMISSION_EMAIL = "ایمیل"
    PROFILE_SUBMISSION_PHONE = "شماره تلفن"
    PROFILE_SUBMISSION_DONE = "✅ اتمام ✅"

    MEDIA_SUBMISSION = "ارسال لینک"
    MEDIA_SUBMISSION_UNIVERSITY = "media_submission_university"
    MEDIA_SUBMISSION_FACULTY = "media_submission_faculty"
    MEDIA_SUBMISSION_OWNER_TITLE = "media_submission_owner_title"
    MEDIA_SUBMISSION_DESCRIPTION = "media_submission_description"
    MEDIA_SUBMISSION_URL = "media_submission_url"
    MEDIA_SUBMISSION_MEDIA_TYPE = "media_submission_media_type"
    MEDIA_SUBMISSION_COURSE = "media_submission_course_stage"
    MEDIA_SUBMISSION_PROFESSOR = "media_submission_professor_stage"
    MEDIA_SUBMISSION_SEMESTER_YEAR = "media_submission_semester_year_stage"

    # ----------------- User Profile Branch -----------------
    # We don't need nodes for this, because we can just send it and interact
    # using InlineKeyboardMarkup.

    # ----------------- Admin Branch -----------------
    ADMIN_PANEL = "admin_panel_stage"
    SHOW_STATISTICS = "show_statistics"
    GET_SUBMISSION_TO_APPROVE = "get_files_to_approve"
    UPDATE_USER_ACCESS = "update_user_access"
    CHOOSE_USER_TO_UPDATE = "choose_user_to_update"
    CHOOSE_USER_ACCESS_LEVEL = "choose_user_access_level"
    # ----------------- Home -----------------
    MY_BOOKMARKS = "پسندهای من"
    SEARCH = "جستجو"
    SUBMIT = "ارسال محتوا"
    MY_PROFILE = "پروفایل من"
    HELP = "راهنما"
    # SUBMIT
    DOCUMENT = "DOCUMENT"
    PROFILE = "PROFILE"
    MEDIA = "MEDIA"
    SUBMISSION_TAG = "SUBMISSION_TAG"
    DOCUMENT_TYPE = "DOCUMENT_TYPE"
    UNIVERSITY = "UNIVERSITY"
    FACULTY = "FACULTY"
    MASTER = "MASTER"
    COURSE_NAME = "COURSE_NAME"
    YEAR = "YEAR"
    WRITER = "WRITER"
    FINISH = "FINISH"
