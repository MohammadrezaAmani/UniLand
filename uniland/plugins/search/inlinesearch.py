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
                    document_file_id=document.file_id,
                    title=record.search_text,
                    id=record.id,
                    caption=document.user_display(),
                    description=f'مورد علاقه {record.likes} نفر',
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(
                                text=f'👍 {record.likes}',
                                callback_data=f"bookmark:{record.id}:{record.likes}"
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
                        document_file_id=profile.image_id,
                        title=record.search_text,
                        id=record.id,
                        caption=profile.user_display(),
                        description=f'مورد علاقه {record.likes} نفر',
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    text=f'👍 {record.likes}',
                                    callback_data=f"bookmark:{record.id}:{record.likes}"
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
                        id=record.id,
                        description=f'مورد علاقه {record.likes} نفر',
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    text=f'👍 {record.likes}',
                                    callback_data=f"bookmark:{record.id}:{record.likes}"
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
                    id=record.id,
                    description=f'مورد علاقه {record.likes} نفر',
                    reply_markup=InlineKeyboardMarkup(
                        [
                                [InlineKeyboardButton(
                                    text=f'👍 {media.likes}',
                                    callback_data=f"bookmark:{record.id}:{record.likes}"
                                )
                                ]
                        ]
                    )
                )
            )

    await inline_query.answer(
        results=results,
        cache_time=1
    )


@Client.on_chosen_inline_result()
async def update_search_stats(client, chosen_inline_result):
    sub_db.increase_search_times(id=int(chosen_inline_result.result_id))


@Client.on_callback_query(filters.regex('^bookmark:'))
async def toggle_user_bookmark(client, callback_query):
    _, sub_id, likes = callback_query.data.split(':')
    sub_id, likes = int(sub_id), int(likes)

    result, new_likes = user_db.toggle_bookmark(
        callback_query.from_user.id, sub_id)

    if result == 0:
        await callback_query.answer('Something Went Wrong!')
        return
    elif new_likes == likes:
        if result == 1:
            await callback_query.answer('Added to bookmarks')
        else:
            await callback_query.answer('Removed from bookmarks')
        return

    await callback_query.edit_message_reply_markup(
        InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=f'👍 {new_likes}',
                        callback_data=f"bookmark:{sub_id}:{new_likes}"
                    )
                ]
            ]
        )
    )
