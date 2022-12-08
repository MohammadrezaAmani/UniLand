import enum

# Messages to be shown in the project


class Messages(enum.Enum):

    HELP_MENU = 'اینجا راهنما است'

    HELP_MENU_SEARCH = 'اینجا راهنمای جستجو است'

    HELP_MENU_SUBMIT = 'اینجا راهنمای ارسال است'

    HELP_MENU_ABOUT_US = 'ما تیم یونی لند هستیم!'

    HELP_MENU_COMING_SOON = 'بزودی...'

  #     ------- MYPROFILE ---------
    # MYPROFILE_NAME = 'نام من' #

    MYPROFILE_SCORE = 'امتیاز: '

    MYPROFILE_SUBMISSIONS = 'ثبت‌شده‌های من'

    SUBMISSIONS_COUNT = 'تعداد ثبت‌ها: '

    MYPROFILE_BOOKMARKS = 'پسند‌های من'  # TODO: bebarid too triggers chon dokmast

    BOOKMARKS_TITLE = 'تعداد پسندها: '
    BOOKMARKS_NOT_FOUND_TITLE = 'شما هیچ پسندی ندارید!'

  #    ----- MISC -----
    DEFAULT_EMPTY_RESULT_TITLE = 'نتیجه ای یافت نشد'
