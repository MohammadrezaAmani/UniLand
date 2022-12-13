import enum


class Triggers(enum.Enum):

    # ----------------- Start -----------------
    START = "/start"
    BACK = "🔙 برگشت"

    # ----------------- Search Branch -----------------

    # ----------------- Submit Branch -----------------
    CHOOSE_SUBMISSION_TYPE = "📤 ارسال محتوا 📤"

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

    MEDIA_SUBMISSION = "ارسال رسانه"
    MEDIA_SUBMISSION_UNIVERSITY = "media_submission_university"
    MEDIA_SUBMISSION_FACULTY = "media_submission_faculty"
    MEDIA_SUBMISSION_OWNER_TITLE = "media_submission_owner_title"
    MEDIA_SUBMISSION_DESCRIPTION = "media_submission_description"
    MEDIA_SUBMISSION_URL = "media_submission_url"
    MEDIA_SUBMISSION_MEDIA_TYPE = "media_submission_media_type"
    MEDIA_SUBMISSION_COURSE = "media_submission_course_stage"
    MEDIA_SUBMISSION_PROFESSOR = "media_submission_professor_stage"
    MEDIA_SUBMISSION_SEMESTER_YEAR = "media_submission_semester_year_stage"

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

    # ----------------- User Profile Branch -----------------
    # We don't need nodes for this, because we can just send it and interact
    # using InlineKeyboardMarkup.

    # ----------------- Admin Branch -----------------
    # SHOW_STATISTICS = "show_statistics" show this on first page of admin panel
    GET_SUBMISSION_TO_APPROVE = "تایید فایل"
    UPDATE_USER_ACCESS = "تغییر سطح دسترسی کاربران"
    ADMIN_EDIT_SUBMISSIONS = "ویرایش فایل ها"
    USER_ACCESS_LEVEL_ADMIN = "ادمین"
    USER_ACCESS_LEVEL_EDITOR = "ادیتور"
    USER_ACCESS_LEVEL_BASIC = "معمولی"

    # ----------------- Home -----------------
    MY_BOOKMARKS = "پسندهای من"  # TO DO: PLACE THIS FIELD IN MYPROFILE FIELD
    SEARCH = "🔍 جستجو 🔎"
    SUBMIT = "📤 ارسال محتوا 📤"
    MY_PROFILE = "👩‍💻 پروفایل من 👨‍💻"
    HELP = "📜 راهنما 📜"
    ADMIN_PANEL = "دسترسی های ویژه"  # only shown to editors & admins

    # -------------- Bookmarks ---------------
    BOOKMARKS_NAV_BACK = '⏮️'   # I'قبلی'I
    BOOKMARKS_NAV_NEXT = '⏭️'  # I'بعدی'I
  
    # -------------- Edit document ----------
    EDIT_SUBMISSION = 'ویرایش اطلاعات'
    EDIT_DOCUMENT_SUBMISSION = 'ویرایش فایل'
    EDIT_DOCUMENT_SUBMISSION_FILE_TYPE = 'ویرایش نوع فایل'
    EDIT_DOCUMENT_SUBMISSION_UNIVERSITY = 'ویرایش دانشگاه'
    EDIT_DOCUMENT_SUBMISSION_FACULTY = 'ویرایش دانشکده'
    EDIT_DOCUMENT_SUBMISSION_OWNER_TITLE = 'ویرایش نام ارسال کننده'
    EDIT_DOCUMENT_SUBMISSION_DESCRIPTION = 'ویرایش توضیحات'
    EDIT_DOCUMENT_SUBMISSION_COURSE = 'ویرایش نام درس'
    EDIT_DOCUMENT_SUBMISSION_PROFESSOR = 'ویرایش نام استاد'
    EDIT_DOCUMENT_SUBMISSION_WRITER = 'ویرایش نام نویسنده'
    EDIT_DOCUMENT_SUBMISSION_SEMESTER_YEAR = 'ویرایش سال تدریس'