from pyrogram import Client, filters
import pyrogram
from uniland.utils import triggers, pages


@Client.on_message(filters.command(["start"]))
async def start_handler(
    client: pyrogram.client.Client,
    message: pyrogram.types.triggers_and_media.message.Message,
):
    """handling start command and adding user to database
        for editing shown text in this method,
        edit uniland/utils/triggers.py
    Args:
        client (pyrogram.client.Client)
        message (pyrogram.types.triggers_and_media.message.Message)
    """
    await client.send_message(
        message.from_user.id,
        triggers.START % (message.from_user.first_name),
        reply_markup=pages.HOME,
    )
