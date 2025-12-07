"""Inline search handler."""
import logging

from pyrogram import Client, filters
from pyrogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InlineQueryResultCachedDocument,
    InputTextMessageContent,
)

from apps.bot.di import get_injector
from apps.bot.utils.keyboards import get_bookmark_keyboard
from apps.search.services import SearchService
from apps.submissions.models import Document, Media, Profile

logger = logging.getLogger(__name__)
injector = get_injector()
search_service = injector.get(SearchService)


@Client.on_inline_query(~filters.bot)
async def inline_search(client: Client, inline_query: InlineQuery):
    """Handle inline search queries."""
    query = inline_query.query.strip()

    if not query or len(query) < 2:
        await inline_query.answer(
            results=[],
            cache_time=1,
            switch_pm_text="Type to search...",
            switch_pm_parameter="start",
        )
        return

    # Perform search
    ignored, submissions = await search_service.search(query, limit=50)

    results = []
    for submission in submissions:
        try:
            if submission.submission_type == "document":
                doc = Document.objects.get(id=submission.id)
                results.append(
                    InlineQueryResultCachedDocument(
                        document_file_id=doc.file_id,
                        title=submission.search_text,
                        id=str(submission.id),
                        caption=doc.user_display() + "\n\n@UniLandBot",
                        description=f"👍 {submission.likes_count} | {submission.description[:100]}",
                        reply_markup=get_bookmark_keyboard(submission.id, submission.likes_count),
                    )
                )

            elif submission.submission_type == "profile":
                profile = Profile.objects.get(id=submission.id)
                if profile.image_id:
                    results.append(
                        InlineQueryResultCachedDocument(
                            document_file_id=profile.image_id,
                            title=submission.search_text,
                            id=str(submission.id),
                            caption=profile.user_display() + "\n\n@UniLandBot",
                            description=f"👍 {submission.likes_count} | {submission.description[:100]}",
                            reply_markup=get_bookmark_keyboard(submission.id, submission.likes_count),
                        )
                    )
                else:
                    results.append(
                        InlineQueryResultArticle(
                            title=submission.search_text,
                            input_message_content=InputTextMessageContent(
                                profile.user_display() + "\n\n@UniLandBot"
                            ),
                            id=str(submission.id),
                            description=f"👍 {submission.likes_count} | {submission.description[:100]}",
                            reply_markup=get_bookmark_keyboard(submission.id, submission.likes_count),
                        )
                    )

            elif submission.submission_type == "media":
                media = Media.objects.get(id=submission.id)
                results.append(
                    InlineQueryResultArticle(
                        title=submission.search_text,
                        input_message_content=InputTextMessageContent(
                            media.user_display() + "\n\n@UniLandBot"
                        ),
                        id=str(submission.id),
                        description=f"👍 {submission.likes_count} | {submission.description[:100]}",
                        reply_markup=get_bookmark_keyboard(submission.id, submission.likes_count),
                    )
                )

        except Exception as e:
            logger.error(f"Error creating inline result for submission {submission.id}: {e}")
            continue

    if not results:
        results.append(
            InlineQueryResultArticle(
                title="No results found",
                description="Try a different search query",
                input_message_content=InputTextMessageContent("No results found for your query."),
                id="-1",
            )
        )

    await inline_query.answer(results=results, cache_time=1)
    logger.info(f"Inline search '{query}' returned {len(results)} results")
