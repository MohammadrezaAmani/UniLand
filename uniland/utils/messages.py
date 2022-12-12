# Messages to be shown in the project

import enum


class Messages(enum.Enum):

    HELP_MENU = 'اینجا راهنما است'

    HELP_MENU_SEARCH = 'اینجا راهنمای جستجو است'

    HELP_MENU_SUBMIT = 'اینجا راهنمای ارسال است'

    HELP_MENU_ABOUT_US = 'ما تیم یونی لند هستیم!'

    HELP_MENU_COMING_SOON = 'بزودی...'

  #     ------- MYPROFILE ---------

    MYPROFILE_ACCESS_LEVEL = '🎚️ سطح دسترسی: '

    MYPROFILE_SCORE = '🎰 امتیاز: '

    SUBMISSIONS_COUNT = '📦 تعداد ثبت‌ها: '

    BOOKMARKS_TITLE = '🖇️ تعداد پسندها: '
    BOOKMARKS_NOT_FOUND_TITLE = 'شما هیچ پسندی ندارید!'

  #    ----- MISC -----
    DEFAULT_EMPTY_RESULT_TITLE = 'نتیجه ای یافت نشد'

  #   ------ ADMIN -----
    ACCESS_LEVEL_BY_USERID = 'یوزر آیدی مورد نظر را وارد کنید: \n میتوانید یوزر آیدی را وارد کنید و یا یک پیام از شخص مورد نظر فوروارد کنید'
    ACCESS_LEVEL_CHOOSE = 'سطح دسترسی مد نظر را وارد کنید: \n\n'
    ACCESS_LEVEL_LEVELS = 'عادی: 1 - ادیتور: 2 - ادمین: 3'
    ACCESS_LEVEL_UPDATED = 'سطح دسترسی کاربر با موفقیت آپدیت شد. \n\n'

    CONFIRMATION_NO_UNCONFIMRED_FILE = "فایل تایید نشده‌ای یافت نشد."
