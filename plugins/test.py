from pyrogram import Client, filters
from uniland.db import dummy

@Client.on_message(filters.text & filters.regex('echo'))
async def echo(client, message):
    await message.reply(message.text)
