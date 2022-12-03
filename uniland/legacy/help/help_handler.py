from pyrogram import Client, filters
import pyrogram
from uniland.utils import messages, pages


@Client.on_message(filters.regex(messages.HELP) | filters.command("help"))
async def document_handler(
    client: pyrogram.client.Client,
    message: pyrogram.types.messages_and_media.message.Message,
):
    """handling help button in bot
        for editing shown text in this method,
        edit uniland/utils/messages.py
    Args:
        client (pyrogram.client.Client) : client
        message (pyrogram.types.messages_and_media.message.Message): message
    """
    await message.reply(text=messages.HELP_DESCRIPTION, reply_markup=pages.BACK)
