from pyrogram import Client, filters
from uniland.utils.filters import admin_only

@Client.on_message(filters.private & admin_only & filters.command('start'))
async def start(client, message):
    await message.reply("You are admin!")

# from pyrogram.handlers import MessageHandler
# import pandas as pd
# from pyrogram.types import (
#     InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton)
# from pyrogram.types import (
#     ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)
# import safebase
# from handlers import app

# @app.on_message(filters.private & filters.command('start') & filters.user(admins_id))
# async def entrance(client, message):
#     print(message.from_user.username)
#     await message.reply(f'You are admin!!!')
#     await message.reply(f'message: {message.text}')
#     await message.reply(f'chat id: {message.chat.id}')
#     await message.reply(f'user id: {message.from_user.id}')
    

# @app.on_message(filters.private & filters.command('keyboard') & filters.user(admins_id))
# async def admin_start(client, message):
#     print(message.from_user.username)
#     await message.reply(f'You are admin!!!')
#     await message.reply(f'message: {message.text}')
#     await message.reply(f'chat id: {message.chat.id}')
#     await message.reply(f'user id: {message.from_user.id}')
    

# @app.on_message(filters.private & filters.text & filters.user(admins_id))
# async def keyboard_test(client, message):
#     chat_id = message.chat.id
#     await app.send_message(
#         chat_id,  # Edit this
#         "This is a ReplyKeyboardMarkup example",
#         reply_markup=ReplyKeyboardMarkup(
#             [
#                 ["A", "B", "C", "D"],  # First row
#                 ["E", "F", "G"],  # Second row
#                 ["H", "I"],  # Third row
#                 ["J"]  # Fourth row
#             ],
#             resize_keyboard=True  # Make the keyboard smaller
#         )
#     )

#     await app.send_message(
#         chat_id,  # Edit this
#         "This is a InlineKeyboardMarkup example",
#         reply_markup=InlineKeyboardMarkup(
#             [
#                 [  # First row
#                     InlineKeyboardButton(  # Generates a callback query when pressed
#                         "Button",
#                         callback_data="data"
#                     ),
#                     InlineKeyboardButton(  # Opens a web URL
#                         "URL",
#                         url="https://docs.pyrogram.org"
#                     ),
#                 ],
#                 [  # Second row
#                     InlineKeyboardButton(  # Opens the inline interface
#                         "Choose chat",
#                         switch_inline_query="pyrogram"
#                     ),
#                     InlineKeyboardButton(  # Opens the inline interface in the current chat
#                         "Inline here",
#                         switch_inline_query_current_chat="pyrogram"
#                     )
#                 ]
#             ]
#         )
#     )

