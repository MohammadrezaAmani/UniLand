from pyrogram import Client, filters
import pyrogram
from uniland.utils import messages,pages

@Client.on_message(filters.regex(messages.BACK))
async def jozve_handler(client, message):
    await message.reply(
            text=messages.BACK_DESCRIPTION,
            reply_markup=pages.HOME
        )
