from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import uniland.db.submission_methods as sub_db
import uniland.db.user_methods as user_db
from uniland import search_engine, usercache
from uniland.config import SEARCH_BACKDOOR_GROUP
from uniland.plugins.start.start import start_stage
from uniland.utils.builders import Builder
from uniland.utils.filters import exact_match, user_step
from uniland.utils.steps import UserSteps
from uniland.utils.triggers import Triggers
from uniland.utils.uxhandler import UXTree


@Client.on_message(
    filters.text & user_step(UserSteps.START.value) & exact_match(Triggers.SEARCH.value)
)
async def get_pv_search_text(client, message):
    # Getting search text from user
    user_step = UXTree.nodes[UserSteps.SEARCH.value]
    await message.reply(text=user_step.description, reply_markup=user_step.keyboard)
    user_db.update_user_step(message.from_user.id, user_step.step)


@Client.on_message(
    filters.text & user_step(UserSteps.SEARCH.value) & ~exact_match(Triggers.BACK.value)
)
async def display_search_result(client, message):
    """
    Display search results based on the user's input.

    Args:
        client: The client object.
        message: The message object.

    Returns:
        None
    """
    if len(message.text) > 100:
        await message.reply(text=".متن جستجو بیش از حد طولانی است")
        return

    search_text = message.text.replace(":", " ")

    ignored, results = search_engine.search(search_text)

    results = [
        Builder.get_submission_child(record.id, record.type) for record in results
    ]

    # TODO! Remove this part...
    try:
        if len(search_text) > 3 and ignored:
            await client.send_message(
                chat_id=SEARCH_BACKDOOR_GROUP,
                text=f"{search_text}\n\n From {message.from_user.first_name}",
            )
    except Exception as e:
        print(e)

    page, page_size = 0, 5
    display_text, buttons = Builder.get_navigation(
        results[page * page_size : min((page + 1) * page_size, len(results))],
        page,
        page_size,
        len(results),
        f"🌐 نتایج جستجو برای {search_text}\n\n",
        lambda sub: sub.user_display(),
        lambda page, page_size: f"pvsearch:{page}:{page_size}:{search_text}",
    )

    await message.reply(
        text=display_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.DISABLED,
        quote=True,
    )
    new_step = UXTree.nodes[UserSteps.SEARCH.value].parent
    if len(results) == 0:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="جستجوی اینلاین", switch_inline_query_current_chat=""
                    )
                ]
            ]
        )
        await message.reply_text(
            text="🕶️ نگران نباش! داریم دنبال فایلت می‌گردیم و به زودی به بات اضافه می‌شه. \nدر ضمن حتما یه سری به نحوه سرچ در بات که توی قسمت راهنما هست بزن! شاید فایلی که می‌خوای رو داشته باشیم ولی درست جستجوش نکردی.",
            reply_markup=keyboard,
        )
    await start_stage(client, message)


@Client.on_callback_query(filters.regex("^pvsearch:"))
async def pvsearch_callback(client, callback_query):
    """
    Callback function for handling the 'pvsearch' command.

    Args:
        client (telegram.Client): The Telegram client.
        callback_query (telegram.CallbackQuery): The callback query object.

    Returns:
        None
    """
    page, page_size, search_text = callback_query.data.split(":")[1:]
    page, page_size = int(page), int(page_size)

    if page < 0:
        await callback_query.answer(text="این صفحه‌ اول است.", show_alert=True)
        return

    ignored, results = search_engine.search(search_text)

    results = [
        Builder.get_submission_child(record.id, record.type) for record in results
    ]

    if len(results) <= page * page_size:
        await callback_query.answer(text="این صفحه آخر است.", show_alert=True)
        return

    display_text, buttons = Builder.get_navigation(
        results[page * page_size : min((page + 1) * page_size, len(results))],
        page,
        page_size,
        len(results),
        f"نتایج جستجو برای {search_text}\n\n",
        lambda sub: sub.user_display(),
        lambda page, page_size: f"pvsearch:{page}:{page_size}:{search_text}",
    )

    await callback_query.edit_message_text(
        display_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.DISABLED,
    )


@Client.on_message(filters.text & filters.regex("^/get_") & ~filters.bot)
async def get_submission(client, message):
    """
    Retrieves a submission based on the provided submission type and ID,
    and sends it as a message to the user.

    Args:
        client: The client instance.
        message: The message object.

    Returns:
        None
    """
    submission_type, submission_id = message.text.split("_")[1:]
    submission = Builder.get_submission_child(submission_id, submission_type)
    if submission == None or not submission.is_confirmed:
        await message.reply(text="این رکورد وجود ندارد.")
        return

    file_id, caption, keyboard = Builder.file_message_generator(submission)
    if not keyboard:
        await message.reply(text="این رکورد وجود ندارد.")
        return

    if submission_type == "document":
        await message.reply_document(
            document=file_id, caption=caption, reply_markup=keyboard
        )
    elif submission_type == "profile":
        if file_id != "":
            await message.reply_document(
                document=file_id, caption=caption, reply_markup=keyboard
            )
        else:
            await message.reply_text(text=caption, reply_markup=keyboard)

    try:
        if not usercache.has_user(message.from_user.id):
            user_db.add_user(message.from_user.id, last_step=UserSteps.START.value)
    except:
        print("None user found in pvsearch")

    sub_db.increase_search_times(id=submission.id)
