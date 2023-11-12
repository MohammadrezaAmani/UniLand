from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from uniland import search_engine, usercache
from uniland.db import user_methods as user_db
from uniland.db import doc_methods as doc_db
from uniland.db import profile_methods as profile_db
from uniland.db import media_methods as media_db
from uniland.db import submission_methods as sub_db
from uniland.utils.uxhandler import UXTree
from uniland.utils.steps import UserSteps
from uniland.utils.pages import Pages


class Builder:
    # TODO use this function
    def display_panel(user_id):
        user_step = UXTree.nodes[UserSteps.ADMIN_PANEL.value]
        if usercache.has_permission(user_id, min_permission=3, max_permission=3):
            output = "🔐 پنل ادمین\n\n"
            output += "📊 آمار ربات:\n"
            output += f"🔎 تعداد کل جستجوها: {search_engine.total_searches}\n\n"
            output += f"👤 تعداد کل کاربران: {user_db.count_users()}\n"
            output += f"👤 تعداد کاربران فعال در یک ساعت اخیر: {user_db.count_active_users(60)}\n"
            output += f"👤 تعداد کاربران فعال در ۲۴ ساعت اخیر: {user_db.count_active_users(60*24)}\n"
            output += f"👤 تعداد کاربران فعال در ۷ روز اخیر: {user_db.count_active_users(60*24*7)}\n"
            output += f"👤 تعداد کاربران جدید در یک ساعت اخیر: {user_db.count_new_signups(60)}\n"
            output += f"👤 تعداد کاربران جدید در ۲۴ ساعت اخیر: {user_db.count_new_signups(60*24)}\n"
            output += f"👤 تعداد کاربران جدید در یک هفته اخیر: {user_db.count_new_signups(60*24*7)}\n\n"

            output += f"👮 تعداد کل ادمین‌ها: {user_db.count_admins()}\n"
            output += f"🕵️ تعداد کل ویرایشگرها: {user_db.count_editors()}\n"
            output += f"🗂️ تعداد رکوردها: {sub_db.count_total_submissions()}\n"
            output += f"🗃️ تعداد رکوردهای تایید شده: {sub_db.count_confirmed_submissions()}\n\n"
            keyboard = user_step.keyboard
        # editor panel
        if usercache.has_permission(user_id, min_permission=2, max_permission=2):
            output = "🔐 وارد پنل ادیتور شدید\n\n"
            keyboard = Pages.EDITOR_PANEL
        return (output, keyboard)

    def get_submission_child(submission_id: int, submission_type: str):
        if submission_type == "document":
            return doc_db.get_document(submission_id)
        elif submission_type == "profile":
            return profile_db.get_profile(submission_id)
        elif submission_type == "media":
            return media_db.get_media(submission_id)
        return None

    def file_message_generator(submission):
        if submission == None:
            return (None, None, None)
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f"👍 {search_engine.get_likes(submission.id)}",
                        callback_data=f"bookmark:{submission.id}:{search_engine.get_likes(submission.id)}",
                    )
                ]
            ]
        )
        text = submission.user_display() + "\n" + "آیدی ربات: @UniLandBot"
        if submission.submission_type == "document":
            return (submission.file_id, text, keyboard)
        if submission.submission_type == "profile":
            return (submission.image_id, text, keyboard)

    def get_navigation(
        submissions: list,
        page: int,
        page_size: int,
        total_size: int,
        page_title: str,
        text_generator,  # lambda sub
        callback_generator,  # lambda sub, page, page_size
    ):
        buttons = [
            [
                InlineKeyboardButton(
                    text="⏮ صفحه قبل",
                    callback_data=callback_generator(page - 1, page_size),
                ),
                InlineKeyboardButton(
                    text="صفحه بعد ⏭",
                    callback_data=callback_generator(page + 1, page_size),
                ),
            ]
        ]

        first = page * page_size + 1
        last = first + len(submissions) - 1
        total = total_size

        # preparing message text
        display_text = page_title
        display_text += f"نتایج {first} تا {last} از {total} رکورد\n"
        for i, submission in enumerate(submissions):
            if not submission:
                display_text += ".رکورد ناموجود است\n\n"

            else:
                display_text += f"\n📔 رکورد {first + i}:\n"
                display_text += text_generator(submission)
                if submission.is_confirmed:
                    display_text += (
                        f"مورد علاقه {search_engine.get_likes(submission.id)} نفر"
                    )
                    display_text += f"\n\n📥 ‌دریافت رکورد: /get_{submission.submission_type}_{submission.id}"
                display_text += "\n\n"
                display_text += 25 * "-"

        return display_text, buttons
