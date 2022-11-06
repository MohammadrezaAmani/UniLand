from pyrogram import Client, filters
from uniland.utils import messages,pages,methods
from uniland.utils.filters import (
    jozve_darkhast, jozve_sabt, jozve_search,
    jozve_check, jozve_react
)
import pyrogram
from uniland.db.db_methods import search_jozve_by_name,search_jozve,add_like


@Client.on_message(filters.regex(messages.JOZVE_TITLE))
async def jozve_handler(client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
    await message.reply(
            text=messages.JOZVE_DESCRIPTION,
            reply_markup=pages.JOZVE
        )
@Client.on_message(filters.regex(messages.JOZVE_SEARCH))
async def jozve_search_handler(client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
    await message.reply(
            text=messages.JOZVE_SEARCH_DESCRIPTION,
            reply_markup=pages.BACK
        )

@Client.on_message(filters.regex(messages.JOZVE_SABT))
async def jozve_sabt_handler(client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
    await message.reply(
            text=messages.JOZVE_SABT_DESCRIPTION,
            reply_markup=pages.JOZVE_SABT
        )

@Client.on_message(filters.regex(messages.JOZVE_DARKHASTI))
async def jozve_darkhast_handler(client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
    await message.reply(
            text=messages.JOZVE_DARKHASTI_DESCRIPTION,
            reply_markup=pages.BACK
        )
@Client.on_message(jozve_darkhast)
async def jozve_darkhast_text_handler(client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
    await methods.send_message_to_admin(client,message)
    await message.reply(
            text=messages.JOZVE_DARKHASTI_CONFIRMATION,
            reply_markup=pages.HOME
        )
@Client.on_message(jozve_search)
async def jozve_search_text_handler(client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
    files = search_jozve_by_name(message.text)
    text = '''🔎 نتایج جستجو برای: %s'''%message.text
    text2='''
_ _ _ _ _ _ _ _ _ _ _ _ _

🎯 %d. %s
استاد: %s
نویسنده: %s
ترم تدریس: %d
📥 download: /bo%d

    '''
    if len(files) == 0:
        text +=' جزوه ای یافت نشد.'
    else:
        number = 1
        for file in files:
            text += text2%(number,file[1],file[2],file[3],file[4],file[0])
    await message.reply(
            text=text,
            reply_markup=pages.BACK
        )

@Client.on_message(jozve_check)
async def jozve_dl_handler(client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
    id = int(message.text.split('bo')[-1])
    file = search_jozve(id)
    text = '''🎯 %d. %s
استاد: %s
نویسنده: %s
ترم تدریس: %d
'''%(file[0],file[2],file[3],file[4],0)
    await message.reply_document(
        file[1],
        quote=True, thumb='AAMCBAADGQEAAgQqY2cJfxSluxQsYJlFcne7cujaDQwAAuoNAALJ1jlTBXMfhIW-2-EACAEAB20ABx4E',caption=text,
        
        reply_markup=pages.LIKE_OR_DISLIKE('jozve',file[0],file[5],file[6])
    )
@Client.on_callback_query(jozve_react)
async def jozve_dl3_handler(client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
    typed,_,id = message.data.split(':')
    add_like(typed,id)
# TODO!: this must me completed
@Client.on_message(jozve_sabt)
async def jozve_sabt_text_handler(client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
    await methods.send_message_to_admin(client,message)
