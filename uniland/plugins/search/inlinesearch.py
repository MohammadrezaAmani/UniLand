# Implementing functionality of bot's inline search
# Implementing functionality of bot's inline search
from pyrogram import Client, filters
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton,
          InlineQueryResultCachedDocument, InlineQueryResultCachedPhoto)

from uniland import search_engine
from uniland.db import user_methods as user_db
from uniland.db import doc_methods as doc_db
from uniland.db import profile_methods as profile_db
from uniland.db import media_methods as media_db
from uniland.db import submission_methods as sub_db

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
            if document == None:
                continue
            results.append(
                InlineQueryResultCachedDocument(
                    document_file_id = document.file_id,
                    title = record.search_text,
                    caption = document.user_display(),
                    description = f'مورد علاقه {record.likes} نفر',
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(
                                text = f'👍 {record.likes}',
                                callback_data = f"bookmark:{inline_query.from_user.id}:{record.id}"
                            )]
                        ]
                    )
                )
            )
        # ---------------------- Profile ----------------------
        elif record.type == 'profile':
            profile = profile_db.get_profile(record.id)
            if profile == None:
                continue
            # ------------- Profile with Photo -------------
            if profile.image_id != None and profile.image_id != '':
                results.append(
                    InlineQueryResultCachedDocument(
                        document_file_id = profile.image_id,
                        title = record.search_text,
                        caption = profile.user_display(),
                        description = f'مورد علاقه {record.likes} نفر',
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    text = f'👍 {record.likes}',
                                    callback_data = f"bookmark:{inline_query.from_user.id}:{record.id}"
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
                            profile.user_display()
                        ),
                        description = f'مورد علاقه {record.likes} نفر',
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    text = f'👍 {record.likes}',
                                    callback_data = f"bookmark:{inline_query.from_user.id}:{record.id}"
                                    )
                                ]
                            ]
                        )
                    )
                )
        
        elif record.type == 'media':
            media = media_db.get_media(record.id)
            if media == None:
                continue
            results.append(
                    InlineQueryResultArticle(
                        title=record.search_text,
                        input_message_content=InputTextMessageContent(
                            media.user_display()
                        ),
                        description = f'مورد علاقه {record.likes} نفر',
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    text = f'👍 {media.likes}',
                                    callback_data = f"bookmark:{inline_query.from_user.id}:{record.id}"
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


@Client.on_callback_query(filters.regex('^bookmark:'))
async def toggle_user_bookmark(client, callback_query):
    args = callback_query.data.split(':')
    # ['bookmark', user_id, record.id]
    result = user_db.toggle_bookmark(int(args[1]), int(args[2]))
    if result == 1: # Submission is bookmarked
        await callback_query.edit_message_reply_markup(
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f'👍 {search_engine.get_likes(int(args[2]))}',
                            callback_data=f"bookmark:{callback_query.from_user.id}:{args[2]}"
                        )
                    ]
                ]
            )
        )
        await callback_query.answer(f'Added to bookmarks')
        return True
    elif result == 0: # Something went Wrong
        await callback_query.answer('Something Went Wrong!')
        return False
    elif result == -1: # Submission removed from bookmards
        await callback_query.edit_message_reply_markup(
            InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f'👍 {search_engine.get_likes(int(args[2]))}',
                            callback_data=f"bookmark:{callback_query.from_user.id}:{args[2]}"
                        )
                    ]
                ]
            )
        )
        await callback_query.answer(f'Removed from bookmarks')
        return True
    # TODO! Change bookmark counts after like button pressed
        
