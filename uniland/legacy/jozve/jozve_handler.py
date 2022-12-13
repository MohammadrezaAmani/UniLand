from pyrogram import Client, filters
from uniland.utils import triggers, pages, methods
from uniland.utils.filters import (
    document_submission,
    document_submission,
    document_search,
    document_check,
    document_react,
    document_submission_no,
)
import pyrogram
from uniland.db.db_methods import search_document_by_name, search_document, add_like


@Client.on_message(filters.regex(triggers.DOCUMENT_TITLE))
async def document_handler(
    client: pyrogram.client.Client,
    message: pyrogram.types.triggers_and_media.message.Message,
):
    await message.reply(text=triggers.DOCUMENT_DESCRIPTION, reply_markup=pages.DOCUMENT)


@Client.on_message(filters.regex(triggers.DOCUMENT_SEARCH))
async def document_search_handler(
    client: pyrogram.client.Client,
    message: pyrogram.types.triggers_and_media.message.Message,
):
    await message.reply(
        text=triggers.DOCUMENT_SEARCH_DESCRIPTION, reply_markup=pages.BACK
    )


@Client.on_message(filters.regex(triggers.DOCUMENT_SUBMISSION))
async def document_submission_handler(
    client: pyrogram.client.Client,
    message: pyrogram.types.triggers_and_media.message.Message,
):
    await message.reply(
        text=triggers.DOCUMENT_SUBMISSION_DESCRIPTION,
        reply_markup=pages.DOCUMENT_SUBMISSION,
    )


@Client.on_message(filters.regex(triggers.DOCUMENT_REQUESTED))
async def document_submission_handler(
    client: pyrogram.client.Client,
    message: pyrogram.types.triggers_and_media.message.Message,
):
    await message.reply(
        text=triggers.DOCUMENT_REQUESTED_DESCRIPTION, reply_markup=pages.BACK
    )


@Client.on_message(document_submission)
async def document_submission_text_handler(
    client: pyrogram.client.Client,
    message: pyrogram.types.triggers_and_media.message.Message,
):
    await methods.send_message_to_admin(client, message)
    await message.reply(
        text=triggers.DOCUMENT_REQUESTED_CONFIRMATION, reply_markup=pages.HOME
    )


@Client.on_message(document_search)
async def document_search_text_handler(
    client: pyrogram.client.Client,
    message: pyrogram.types.triggers_and_media.message.Message,
):
    files = search_document_by_name(message.text)
    text = """🔎 نتایج جستجو برای: %s""" % message.text
    text2 = """
_ _ _ _ _ _ _ _ _ _ _ _ _

🎯 %d. %s
استاد: %s
نویسنده: %s
ترم تدریس: %d
📥 download: /bo%d

    """
    if len(files) == 0:
        text += " جزوه ای یافت نشد."
    else:
        number = 1
        for file in files:
            text += text2 % (number, file[1], file[2], file[3], file[4], file[0])
    await message.reply(text=text, reply_markup=pages.BACK)


@Client.on_message(document_check)
async def document_dl_handler(
    client: pyrogram.client.Client,
    message: pyrogram.types.triggers_and_media.message.Message,
):
    id = int(message.text.split("bo")[-1])
    file = search_document(id)
    text = """🎯 %d. %s
استاد: %s
نویسنده: %s
ترم تدریس: %d
""" % (
        file[0],
        file[2],
        file[3],
        file[4],
        0,
    )
    await message.reply_document(
        file[1],
        quote=True,
        thumb="AAMCBAADGQEAAgQqY2cJfxSluxQsYJlFcne7cujaDQwAAuoNAALJ1jlTBXMfhIW-2-EACAEAB20ABx4E",
        caption=text,
        reply_markup=pages.LIKE_OR_DISLIKE("document", file[0], file[5], file[6]),
    )


@Client.on_callback_query(document_react)
async def document_dl3_handler(
    client: pyrogram.client.Client,
    message: pyrogram.types.triggers_and_media.message.Message,
):
    typed, _, id = message.data.split(":")
    add_like(typed, id)


@Client.on_callback_query(document_submission_no)
async def document_submission_no_handler(
    client: pyrogram.client.Client,
    message: pyrogram.types.triggers_and_media.message.Message,
):
    print(message)


# TODO!: this must me completed
@Client.on_message(document_submission)
async def document_submission_text_handler(
    client: pyrogram.client.Client,
    message: pyrogram.types.triggers_and_media.message.Message,
):
    await methods.send_message_to_admin(client, message)
