from pyrogram import Client, filters
from uniland.utils.filters import admin_only
from uniland.db import admin as admin_db

@Client.on_message(filters.private & ~admin_only & filters.command('start'))
async def start(client, message):
    # for admin in admin_db.list_admins():
    #     await message.reply(str(admin))
    await message.reply("You are not admin:(")
    

# class UsersHandler():
    
#     def __init__(self, app, admins_id):
#         self.app = app
#         self.admins_id = admins_id
        
#     @self.app.on_message(filters.private & filters.text & (~filters.user(admins_id)))
#     async def user_start(client, message):
#         await message.reply(f'message: {message.text}')
#         await message.reply(f'chat id: {message.chat.id}')
#         await message.reply(f'user id: {message.from_user.id}')
