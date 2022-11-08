from pyrogram import Client, filters
# from uniland.utils.filters import access_level
# from uniland.db.tables import User
# from uniland.db import user_methods as user_db

# This file tests bot uptime

@Client.on_message(filters.text & filters.regex('echo'))
async def echo(client, message):
    await message.reply(message.text)

# @Client.on_message(filters.text & filters.command('add_me'))
# async def addme(client, message):
#     user = User(message.from_user.id)
#     print(message.from_user.id)
#     await message.reply('Done!')
    
    
# @Client.on_message(filters.text & filters.command('list_all'))
# async def listall(client, message):
#     users = user_db.list_users()
#     for user in users:
#         await message.reply(str(user))
