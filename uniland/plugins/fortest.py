from pyrogram import Client, filters
from uniland.db.tables import User
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from uniland.db import user_methods as user_db
from uniland.db import doc_methods as doc_db
from uniland.db import profile_methods as profile_db
from uniland.db import media_methods as media_db
from uniland import search_engine, usercache
from uniland.utils.filters import access_level, user_step
from uniland.utils.builders import Builder
from uniland.config import STORAGE_CHAT_ID

# @Client.on_message(filters.photo)
# async def mime_type(client, message):
#     photo = await message.download(in_memory=True)
#     sent_message = await client.send_document(
#         chat_id=STORAGE_CHAT_ID,
#         document=photo
#     )
#     image_id = sent_message.document.file_id
#     await message.reply_document(image_id)


@Client.on_message(
    filters.text & filters.command("send_db") & access_level(3, 3), group=2
)
async def send_db(client, message):
    subs = len(search_engine.subs)
    await message.reply_document(
        "AUT_Archive.sqlite", caption=f"Total confirmed submissions: {subs}"
    )


@Client.on_message(
    filters.text & filters.command("count_actives") & access_level(3, 3), group=2
)
async def count_actives(client, message):
    await message.reply_text(
        f"Total active users in last hour: {user_db.count_active_users(60)}"
    )


@Client.on_message(filters.text & filters.command("broadcast") & access_level(3, 3))
async def public_announcement(client, message):
    user_ids = usercache.users.keys()
    message.text = message.text.replace("/broadcast", "")
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="جستجوی اینلاین", switch_inline_query_current_chat=""
                )
            ]
        ]
    )
    good, bad = 0, 0
    for user_id in user_ids:
        try:
            await message.copy(chat_id=user_id, reply_markup=keyboard)
            good += 1
            # await client.send_message(user.user_id, text)
        except:
            bad += 1
    await message.reply_text(
        f"Total number of users : {good+bad}\nSuccessful: {good}\nFailed: {bad}"
    )


@Client.on_message(access_level(3, 3) & filters.command("chat_details"))
async def display_details(client, message):
    await message.reply_text(
        f"Chat ID: {message.chat.id}, Chat Type: {message.chat.type}"
    )
    await message.reply_text(f"User ID: {message.from_user.id}")


@Client.on_message(filters.text & filters.regex("admin") & access_level(min=3))
async def admin_check(client, message):
    await message.reply("You are admin")


# @Client.on_message(filters.text & filters.regex('step') & user_step('test'))
# async def step_check(client, message):
#   await message.reply("You are in test step")


@Client.on_message(access_level(3, 3) & filters.text & filters.regex("echo"))
async def echo(client, message):
    await message.reply(message.text)
    await message.reply("from UniLand!")


# @Client.on_message(filters.text & filters.regex('search'))
# async def search(client, message):
#   text = message.text.replace('search', '')
#   for record in search_engine.search(text):
#     await message.reply(str(record))

# @Client.on_message(filters.text & filters.command('add_me'))
# async def addme(client, message):
#   user = User(message.from_user.id)
#   print(message.from_user.id)
#   user_db.add_user(message.from_user.id)
#   await message.reply('Done!')


@Client.on_message(access_level(3, 3) & filters.text & filters.command("list_all"))
async def listall(client, message):
    users = user_db.list_users()
    await message.reply("Fetched Users!")
    print(users)
    for user in users:
        await message.reply(str(user))


# @Client.on_message(filters.text & filters.command('test_doc'))
# async def testdoc(client, message):
#   await message.reply('Testing...')
#   doc_db.add_document(message.from_user.id)
#   await message.reply('Document Added!')


@Client.on_message(filters.text & filters.command("list_doc") & access_level(3, 3))
async def listdoc(client, message):
    await message.reply("Testing...")
    docs = doc_db.list_documents()
    for doc in docs:
        await message.reply(str(doc))
    await message.reply("End of the list")


# @Client.on_message(filters.text & filters.command('test_profile'))
# async def testprofile(client, message):
#   await message.reply('Testing...')
#   profile_db.add_profile(message.from_user.id)
#   await message.reply('Profile Added!')


@Client.on_message(filters.text & filters.command("list_profile") & access_level(3, 3))
async def listprofile(client, message):
    await message.reply("Testing...")
    profiles = profile_db.list_profiles()
    for profile in profiles:
        await message.reply(str(profile))
    await message.reply("End of the list")


# @Client.on_message(filters.text & filters.command('test_media'))
# async def testmedia(client, message):
#   await message.reply('Testing...')
#   media_db.add_media(message.from_user.id)
#   await message.reply('Media Added!')


@Client.on_message(filters.text & filters.command("list_media") & access_level(3, 3))
async def listmedia(client, message):
    await message.reply("Testing...")
    medias = media_db.list_medias()
    for media in medias:
        await message.reply(str(media))
    await message.reply("End of the list")
