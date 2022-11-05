# from uniland import UniLand
from pyrogram import Client


if __name__ == "__main__":
    Client(
        "uniland",
        plugins = dict(root='uniland.plugins'),
    ).run()
