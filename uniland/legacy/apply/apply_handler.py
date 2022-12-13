# TODO: completing this option

from pyrogram import Client, filters
import pyrogram
from uniland.utils import triggers, pages


@Client.on_message(filters.regex(triggers.APPLY))
async def apply_handler(
    client: pyrogram.client.Client,
    message: pyrogram.types.triggers_and_media.message.Message,
):
    """handling apply button in bot
        for editing shown text in this method,
        edit uniland/utils/triggers.py
    Args:
        client (pyrogram.client.Client) : client
        message (pyrogram.types.triggers_and_media.message.Message): message
    """
    await message.reply(text=triggers.COMMING_SOON, reply_markup=pages.BACK)
