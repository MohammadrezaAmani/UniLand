"""Search API views."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.search.services import SearchService
from apps.submissions.serializers import SubmissionSerializer


class SearchView(APIView):
    """Search submissions API."""

    def get(self, request):
        """Search for submissions."""
        query = request.query_params.get("q", "")
        limit = int(request.query_params.get("limit", 50))

        if not query:
            return Response(
                {"error": "Query parameter 'q' is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        search_service = SearchService()
        ignored, results = search_service.search(query, limit)

        serializer = SubmissionSerializer(results, many=True)
        return Response(
            {
                "query": query,
                "count": len(results),
                "ignored_words": ignored,
                "results": serializer.data,
            }
        )


class PopularSearchesView(APIView):
    """Get popular search queries."""

    def get(self, request):
        """Get popular searches."""
        limit = int(request.query_params.get("limit", 10))
        search_service = SearchService()
        popular = search_service.get_popular_searches(limit)

        return Response({"popular_searches": popular})
