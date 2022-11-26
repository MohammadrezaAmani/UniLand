# from uniland import UniLand
from uniland import search_engine, SESSION
from uniland.db.tables import Submission
from pyrogram import Client
from .config import API_ID, API_HASH, BOT_TOKEN

if __name__ == "__main__":
    
    plugins = dict(
        root='uniland.plugins',
        # include=[
        #     'jozve.jozve_handler',
        #     'start.start_handler',
        #     'back.back_handler',
        #     'help.help_handler',
        #     'ostad.ostad_handler',
        #     'apply.apply_handler',
        #     'reserve.reserve_handler',
        #     'test'
        #     ]
        )
    
    Client(
        "UniLand",
        api_id = API_ID,
        api_hash = API_HASH,
        bot_token = BOT_TOKEN,
        plugins = plugins
    ).run()
