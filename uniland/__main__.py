from pyrogram import Client
from .config import API_ID, API_HASH, BOT_TOKEN

if __name__ == "__main__":

    plugins = dict(
        root="uniland.plugins",
        include=[
            # Test plugin for testing functionalities
            "fortest",
            # 'uniland.plugins.start folder'
            "start.start",
            # 'uniland.plugins.submission folder'
            "submission.document",
            "submission.media",
            "submission.profile",
            "submission.submission",
            # 'uniland.plugins.search folder'
            "search.inlinesearch",
            "search.pvsearch",
            # 'uniland.plugins.admin folder'
            "admin.access",
            "admin.confirmation",
            "admin.access",
            "back.back_handler",
        ],
    )

    Client(
        "UniLand",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=plugins,
        proxy=dict(scheme="socks5", hostname="127.0.0.1", port=1089),
    ).run()
