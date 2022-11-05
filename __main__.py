# from uniland import UniLand
from pyrogram import Client

# from .config import API_ID, API_HASH, BOT_TOKEN

if __name__ == "__main__":
    Client(
        "uniland",
        plugins = dict(root='uniland.plugins'),
        # proxy=dict(scheme='socks5', hostname='127.0.0.1', port=7060)
    ).run()
