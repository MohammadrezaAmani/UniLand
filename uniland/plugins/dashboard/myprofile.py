from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from uniland import usercache
from uniland.db import user_methods as user_db
from uniland.utils.builders import Builder
from uniland.utils.filters import exact_match, user_step
from uniland.utils.messages import Messages
from uniland.utils.steps import UserSteps
from uniland.utils.triggers import Triggers


@Client.on_message(
    filters.text
    & user_step(UserSteps.START.value)
    & exact_match(Triggers.MY_PROFILE.value)
)
async def show_user_profile(client, message):
    buttons = [
        [
            InlineKeyboardButton(
                text="🔖 نمایش پسندها",
                callback_data=f"showbookmarks:{message.from_user.id}:0:5",
            )
        ],
        [
            InlineKeyboardButton(
                text="🗄️ نمایش فایل‌های من",
                callback_data=f"showmysubs:{message.from_user.id}:0:5",
            )
        ],
    ]

    user_id = message.from_user.id
    score_message = (
        Messages.MYPROFILE_SCORE.value
        + str(
            usercache.get_achieved_likes(user_id)
            + 5 * user_db.count_user_submissions(user_id)
        )
        + " ("
        + str(user_db.count_user_submissions(user_id))
        + " فایل ثبت شده، هریک 5 امتیاز و "
        + str(usercache.get_achieved_likes(user_id))
        + " لایک توسط کاربران"
        + ")"
        + "\n\n"
    )
    submitted_message = (
        Messages.SUBMISSIONS_COUNT.value
        + str(user_db.count_user_submissions(user_id))
        + "\n\n"
    )
    bookmark_message = (
        Messages.BOOKMARKS_TITLE.value
        + str(user_db.count_user_bookmarks(user_id))
        + "\n\n"
    )
    access_level_message = Messages.MYPROFILE_ACCESS_LEVEL.value + " " + "\n\n"
    if usercache.has_permission(
        message.from_user.id, min_permission=3, max_permission=3
    ):
        access_level_message = Messages.MYPROFILE_ACCESS_LEVEL.value + "ادمین" + "\n\n"
    elif usercache.has_permission(
        message.from_user.id, min_permission=2, max_permission=2
    ):
        access_level_message = (
            Messages.MYPROFILE_ACCESS_LEVEL.value + "ویرایشگر" + "\n\n"
        )
    elif usercache.has_permission(
        message.from_user.id, min_permission=1, max_permission=1
    ):
        access_level_message = (
            Messages.MYPROFILE_ACCESS_LEVEL.value + "کاربر عادی" + "\n\n"
        )

    final_message = (
        access_level_message + score_message + submitted_message + bookmark_message
    )
    await message.reply(text=final_message, reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex("^myprofile"))
async def show_myprofile(client, callback_query):
    buttons = [
        [
            InlineKeyboardButton(
                text="🔖 نمایش پسندهای من",
                callback_data=f"showbookmarks:{callback_query.from_user.id}:0:5",
            )
        ],
        [
            InlineKeyboardButton(
                text="🗄️ نمایش فایل‌های من",
                callback_data=f"showmysubs:{callback_query.from_user.id}:0:5",
            )
        ],
    ]

    user_id = callback_query.from_user.id
    score_message = (
        Messages.MYPROFILE_SCORE.value
        + str(
            usercache.get_achieved_likes(user_id)
            + 5 * user_db.count_user_submissions(user_id)
        )
        + " ("
        + str(user_db.count_user_submissions(user_id))
        + " فایل ثبت شده، هریک 5 امتیاز و "
        + str(usercache.get_achieved_likes(user_id))
        + " لایک توسط کاربران"
        + ")"
        + "\n\n"
    )
    submitted_message = (
        Messages.SUBMISSIONS_COUNT.value
        + str(user_db.count_user_submissions(user_id))
        + "\n\n"
    )
    bookmark_message = (
        Messages.BOOKMARKS_TITLE.value
        + str(user_db.count_user_bookmarks(user_id))
        + "\n\n"
    )
    access_level_message = Messages.MYPROFILE_ACCESS_LEVEL.value + " " + "\n\n"
    if usercache.has_permission(
        callback_query.from_user.id, min_permission=3, max_permission=3
    ):
        access_level_message = Messages.MYPROFILE_ACCESS_LEVEL.value + "ادمین" + "\n\n"
    elif usercache.has_permission(
        callback_query.from_user.id, min_permission=2, max_permission=2
    ):
        access_level_message = (
            Messages.MYPROFILE_ACCESS_LEVEL.value + "ویرایشگر" + "\n\n"
        )
    elif usercache.has_permission(
        callback_query.from_user.id, min_permission=1, max_permission=1
    ):
        access_level_message = (
            Messages.MYPROFILE_ACCESS_LEVEL.value + "کاربر عادی" + "\n\n"
        )

    final_message = (
        access_level_message + score_message + submitted_message + bookmark_message
    )
    await callback_query.edit_message_text(
        text=final_message, reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_callback_query(filters.regex("^showbookmarks:"))
async def show_bookmarks_callback(client, callback_query):
    user_id, page, page_size = list(map(int, callback_query.data.split(":")[1:]))

    if page < 0:
        await callback_query.answer(text="این صفحه اول است.", show_alert=True)
        return

    results = user_db.get_user_bookmarks(user_id)

    if len(results) == 0:
        await callback_query.answer(
            text="شما هنوز محتوایی را پسند نکرده‌اید.", show_alert=True
        )
        return

    if len(results) <= page * page_size:
        await callback_query.answer(text="این صفحه آخر است.", show_alert=True)
        return

    display_text, buttons = Builder.get_navigation(
        results[page * page_size : min((page + 1) * page_size, len(results))],
        page,
        page_size,
        len(results),
        "🔖پسندهای شما\n\n",
        lambda sub: sub.user_display(),
        lambda page, page_size: f"showbookmarks:{user_id}:{page}:{page_size}",
    )

    if not display_text or not buttons:
        await callback_query.answer(text="این صفحه آخر است.", show_alert=True)
        return

    buttons.append(
        [InlineKeyboardButton(text="بازگشت به پروفایل من", callback_data="myprofile")]
    )

    await callback_query.edit_message_text(
        display_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.DISABLED,
    )


@Client.on_callback_query(filters.regex("^showmysubs:"))
async def show_mysubs_callback(client, callback_query):
    user_id, page, page_size = list(map(int, callback_query.data.split(":")[1:]))

    if page < 0:
        await callback_query.answer(text="این صفحه اول است.", show_alert=True)
        return

    results = user_db.get_user_submissions(user_id)

    if len(results) == 0:
        await callback_query.answer(
            text="شما هنوز محتوایی را ثبت نکرده‌اید.", show_alert=True
        )
        return

    if len(results) <= page * page_size:
        await callback_query.answer(text="این صفحه آخر است.", show_alert=True)
        return

    types = {"document": "فایل", "profile": "پروفایل", "media": "رسانه"}

    display_text, buttons = Builder.get_navigation(
        results[page * page_size : min((page + 1) * page_size, len(results))],
        page,
        page_size,
        len(results),
        "🗄️فایل‌های ثبت شده توسط شما\n\n",
        lambda sub: f"{'✅' if sub.is_confirmed else '❌'} "
        f"{types[sub.submission_type]}:\n"
        f"{sub.user_display()}",
        lambda page, page_size: f"showmysubs:{user_id}:{page}:{page_size}",
    )

    if not display_text or not buttons:
        await callback_query.answer(text="این صفحه آخر است.", show_alert=True)
        return

    buttons.append(
        [InlineKeyboardButton(text="بازگشت به پروفایل من", callback_data="myprofile")]
    )

    await callback_query.edit_message_text(
        display_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.DISABLED,
    )
