# from pyrogram import Client, filters
# from uniland.utils.triggers import Triggers
# import uniland.db.user_methods as user_db
# import uniland.db.doc_methods as doc_db
# from uniland.db.tables import Document
# from uniland.utils.steps import UserSteps
# from uniland.utils.uxhandler import UXTree
# from uniland.utils.filters import user_step, exact_match
# from uniland.utils.enums import DocType
# from uniland.config import STORAGE_CHAT_ID


# @Client.on_message(filters.text & ~filters.me & exact_match(Triggers.SEARCH.value)
#                    & user_step(UserSteps.START.value))
# async def get_search_text(client, message):
#     # Getting search text from user
#     user_step = UXTree.nodes[UserSteps.SEARCH.value]
#     await message.reply(text=user_step.description, reply_markup=user_step.keyboard)
#     user_db.update_user_step(message.from_user.id, UserSteps.SEARCH.value)


# @Client.on_message(filters.text and filters.private and
#                    user_step(UserSteps.SEARCH.value) and
#                    ~exact_match(Triggers.BACK.value))
# async def echo_search(client, message):
#     # echo users search text
#     #TODO replace with appropriate method
#     user_step = UXTree.nodes[UserSteps.SEARCH_SHOW_RESULTS]
#     await message.reply(text=message.text,
#                         reply_markup=user_step.keyboard)
#     user_db.update_user_step(message.from_user.id,
#                              UserSteps.SEARCH_SHOW_RESULTS.value)
