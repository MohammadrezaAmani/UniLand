from pyrogram import Client, filters
from uniland.utils import messages,pages
@Client.on_message(filters.text & filters.regex('echo'))
async def echo(client, message):
    await message.reply(message.text)

@Client.on_message(filters.regex(messages.JOZVE_TITLE))
async def jozve_handler(client, message):
    await message.reply(
            text=messages.JOZVE_DESCRIPTION,
            reply_markup=pages.JOZVE
        )