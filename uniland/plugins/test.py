from pyrogram import Client, filters
# from uniland.utils.filters import access_level
from uniland.db.tables import User
from uniland.db import tables
from uniland.db import user_methods as user_db
from uniland.db import doc_methods as doc_db
from uniland.db import profile_methods as profile_db
from uniland.db import media_methods as media_db
from uniland import search_engine
from uniland.utils.filters import access_level

# This file tests bot uptime

@Client.on_message(filters.text & filters.regex('admin') & access_level(min=3))
async def admin_check(client, message):
  await message.reply("You are admin")

@Client.on_message(filters.text & filters.regex('echo'))
async def echo(client, message):
  await message.reply(message.text)

@Client.on_message(filters.text & filters.regex('search'))
async def search(client, message):
  text = message.text.replace('search', '')
  for record in search_engine.search(text):
    await message.reply(str(record))

@Client.on_message(filters.text & filters.command('add_me'))
async def addme(client, message):
    user = User(message.from_user.id)
    print(message.from_user.id)
    user_db.add_user(message.from_user.id)
    await message.reply('Done!')
    
    
@Client.on_message(filters.text & filters.command('list_all'))
async def listall(client, message):
    users = user_db.list_users()
    await message.reply('Fetched Users!')
    print(users)
    for user in users:
        await message.reply(str(user))
        
@Client.on_message(filters.text & filters.command('test_doc'))
async def testdoc(client, message):
    await message.reply('Testing...')
    doc_db.add_document(message.from_user.id)
    await message.reply('Document Added!')
    

@Client.on_message(filters.text & filters.command('list_doc'))
async def listdoc(client, message):
    await message.reply('Testing...')
    docs = doc_db.list_documents()
    for doc in docs:
        await message.reply(str(doc))
    await message.reply('End of the list')
    

@Client.on_message(filters.text & filters.command('test_profile'))
async def testprofile(client, message):
    await message.reply('Testing...')
    profile_db.add_profile(message.from_user.id)
    await message.reply('Profile Added!')


@Client.on_message(filters.text & filters.command('list_profile'))
async def listprofile(client, message):
    await message.reply('Testing...')
    profiles = profile_db.list_profiles()
    for profile in profiles:
        await message.reply(str(profile))
    await message.reply('End of the list')
    
@Client.on_message(filters.text & filters.command('test_media'))
async def testmedia(client, message):
    await message.reply('Testing...')
    media_db.add_media(message.from_user.id)
    await message.reply('Media Added!')


@Client.on_message(filters.text & filters.command('list_media'))
async def listmedia(client, message):
    await message.reply('Testing...')
    medias = media_db.list_medias()
    for media in medias:
        await message.reply(str(media))
    await message.reply('End of the list')
