"""Search service with Redis-based indexing."""
import logging
from typing import List, Tuple

from asgiref.sync import sync_to_async
from django.core.cache import cache
from django.db.models import Q

from apps.submissions.models import Submission

logger = logging.getLogger(__name__)


class SearchService:
    """Fast search service using Redis and PostgreSQL full-text search."""

    CACHE_PREFIX = "search"
    CACHE_TTL = 300  # 5 minutes

    def _get_cache_key(self, query: str) -> str:
        """Get cache key for search query."""
        return f"{self.CACHE_PREFIX}:{query.lower()}"

    @sync_to_async
    def search(self, query: str, limit: int = 50) -> Tuple[bool, List[Submission]]:
        """
        Search for submissions.

        Returns:
            Tuple of (ignored_words, results)
        """
        if not query or len(query) < 2:
            return (False, [])

        # Check cache first
        cache_key = self._get_cache_key(query)
        cached_results = cache.get(cache_key)
        if cached_results is not None:
            return cached_results

        # Perform search
        query_lower = query.lower().strip()
        words = query_lower.split()

        # Build Q objects for search
        q_objects = Q()
        for word in words:
            q_objects |= Q(search_text__icontains=word)

        # Execute search
        results = list(
            Submission.objects.filter(
                q_objects,
                is_confirmed=True,
                is_deleted=False,
            )
            .select_related("owner")
            .order_by("-likes_count", "-search_times")[:limit]
        )

        # Cache results
        cache.set(cache_key, (False, results), self.CACHE_TTL)

        logger.info(f"Search query '{query}' returned {len(results)} results")
        return (False, results)

    @sync_to_async
    def index_submission(self, submission: Submission):
        """Index a submission for search."""
        # Clear related caches
        cache.delete_pattern(f"{self.CACHE_PREFIX}:*")
        logger.debug(f"Indexed submission {submission.id}")

    @sync_to_async
    def remove_from_index(self, submission_id: int):
        """Remove submission from search index."""
        cache.delete_pattern(f"{self.CACHE_PREFIX}:*")
        logger.debug(f"Removed submission {submission_id} from index")

    @sync_to_async
    def get_popular_searches(self, limit: int = 10) -> List[str]:
        """Get popular search queries."""
        # This would typically come from analytics
        return []

    @sync_to_async
    def increment_search_count(self, submission_id: int):
        """Increment search count for a submission."""
        Submission.objects.filter(id=submission_id).update(
            search_times=models.F("search_times") + 1
        )
