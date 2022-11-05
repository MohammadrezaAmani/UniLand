# from uniland import UniLand
from pyrogram import Client
#! create file with name config.py and replace your api_id, api_hash, bot token and DB_URI
#? API_ID = 'api_id'
#? API_HASH = 'api_hash'
#? BOT_TOKEN = 'bot_token'
#? DB_URI = 'db_uri'

# DB_URI = 'sqlite:///AUT_Archive.sqlite'
from .config import API_ID, API_HASH, BOT_TOKEN

if __name__ == "__main__":
    Client(
        "Uniland Bot",
        api_id = API_ID,
        api_hash = API_HASH,
        bot_token = BOT_TOKEN,
        plugins = dict(root='uniland.plugins'),
        proxy=dict(scheme='socks5', hostname='127.0.0.1', port=7060)
    ).run()
