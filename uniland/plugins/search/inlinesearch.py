# Implementing functionality of bot's inline search
# Implementing functionality of bot's inline search
from pyrogram import Client

from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton,
          InlineQueryResultCachedDocument, InlineQueryResultCachedPhoto)

from uniland import search_engine
from uniland.db import doc_methods as doc_db
from uniland.db import profile_methods as profile_db
from uniland.db import media_methods as media_db

@Client.on_inline_query()
async def answer(client, inline_query):
    records = search_engine.search(inline_query.query)
    
    # Make 5 example SubmissionRecord objects in records list
    # records = [
    #     SubmissionRecord(i, f'Doc{i}', 'document', i*2,
    #                      file_id='BQACAgQAAxkBAAII7GOKX-QAAXUuH0zT7AABKn1hmkMVCYYAAjgOAAJ6SRlQ0CNPvxG1_-8eBA')
    #     for i in range (5)
    # ]
    
    results = []
    for record in records:
        # ---------------------- Document ----------------------
        if record.type == 'document':
            document = doc_db.get_document(record.id)
            results.append(
                InlineQueryResultCachedDocument(
                    document_file_id = document.file_id,
                    title = record.search_text,
                    caption = str(document),
                    description = f'مورد علاقه {record.likes} نفر',
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(
                                text = '👍',
                                callback_data = f"bookmark:{inline_query.from_user.id}:{record.id}:{record.type}"
                            )]
                        ]
                    )
                )
            )
        # ---------------------- Profile ----------------------
        elif record.type == 'profile':
            profile = profile_db.get_profile(record.id)
            # ------------- Profile with Photo -------------
            if profile.image_id != '':
                results.append(
                    InlineQueryResultCachedPhoto(
                        photo_file_id = profile.image_id,
                        title = record.search_text,
                        caption = str(profile),
                        description = f'مورد علاقه {record.likes} نفر',
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    text = '👍',
                                    callback_data = f"bookmark:{inline_query.from_user.id}:{record.id}:{record.type}"
                                )]
                            ]
                        )
                    )
                )
            # ------------- Profile without Photo -------------
            else:
                results.append(
                    InlineQueryResultArticle(
                        title=record.search_text,
                        input_message_content=InputTextMessageContent(
                            str(profile)
                        ),
                        description = f'مورد علاقه {record.likes} نفر',
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    text = '👍',
                                    callback_data = f"bookmark:{inline_query.from_user.id}:{record.id}:{record.type}"
                                )
                            ]
                       ]
                    )
                )
                )
        
        elif record.type == 'media':
            media = media_db.get_media(record.id)
            results.append(
                    InlineQueryResultArticle(
                        title=record.search_text,
                        input_message_content=InputTextMessageContent(
                            str(media)
                        ),
                        description = f'مورد علاقه {record.likes} نفر',
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    text = '👍',
                                    callback_data = f"bookmark:{inline_query.from_user.id}:{record.id}:{record.type}"
                                )
                            ]
                            ]
                        )
                    )
                )
    
    await inline_query.answer(
        results = results,
        cache_time = 1
    )


# @Client.on_inline_query()
# async def answer(client, inline_query):
#     await inline_query.answer(
#         results=[
#             InlineQueryResultArticle(
#                 title="Installation",
#                 input_message_content=InputTextMessageContent(
#                     "Here's how to install **Pyrogram**"
#                 ),
#                 url="https://docs.pyrogram.org/intro/install",
#                 description="How to install Pyrogram",
#                 reply_markup=InlineKeyboardMarkup(
#                     [
#                         [InlineKeyboardButton(
#                             "Open website",
#                             url="https://docs.pyrogram.org/intro/install"
#                         )]
#                     ]
#                 )
#             ),
#             InlineQueryResultArticle(
#                 title="Usage",
#                 input_message_content=InputTextMessageContent(
#                     "Here's how to use **Pyrogram**"
#                 ),
#                 url="https://docs.pyrogram.org/start/invoking",
#                 description="How to use Pyrogram",
#                 reply_markup=InlineKeyboardMarkup(
#                     [
#                         [InlineKeyboardButton(
#                             "Open website",
#                             url="https://docs.pyrogram.org/start/invoking"
#                         )]
#                     ]
#                 )
#             )
#         ],
#         cache_time=1
#     )
