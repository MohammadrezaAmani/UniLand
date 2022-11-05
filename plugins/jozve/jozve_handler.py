from pyrogram import Client, filters
from uniland.utils import messages,pages,methods
from uniland.utils.filters import jozve_darkhast, jozve_sabt, jozve_search

@Client.on_message(filters.regex(messages.JOZVE_TITLE))
async def jozve_handler(client, message):
    await message.reply(
            text=messages.JOZVE_DESCRIPTION,
            reply_markup=pages.JOZVE
        )
@Client.on_message(filters.regex(messages.JOZVE_SEARCH))
async def jozve_search_handler(client, message):
    await message.reply(
            text=messages.JOZVE_SEARCH_DESCRIPTION,
            reply_markup=pages.BACK
        )

@Client.on_message(filters.regex(messages.JOZVE_SABT))
async def jozve_sabt_handler(client, message):
    await message.reply(
            text=messages.JOZVE_SABT_DESCRIPTION,
            reply_markup=pages.JOZVE_SABT
        )

@Client.on_message(filters.regex(messages.JOZVE_DARKHASTI))
async def jozve_darkhast_handler(client, message):
    await message.reply(
            text=messages.JOZVE_DARKHASTI_DESCRIPTION,
            reply_markup=pages.BACK
        )
@Client.on_message(jozve_darkhast)
async def jozve_darkhast_text_handler(client, message):
    await methods.send_message_to_admin(client,message)
@Client.on_message(jozve_search)
async def jozve_search_text_handler(client, message):
    await methods.send_message_to_admin(client,message)
@Client.on_message(jozve_sabt)
async def jozve_sabt_text_handler(client, message):
    await methods.send_message_to_admin(client,message)
