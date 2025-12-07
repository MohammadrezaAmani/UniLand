"""User API views."""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.submissions.models import Bookmark
from apps.users.models import User
from apps.users.serializers import UserSerializer, UserStatsSerializer


class CurrentUserView(APIView):
    """Get current user information."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current user."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserDetailView(APIView):
    """Get user details by Telegram ID."""

    permission_classes = [IsAuthenticated]

    def get(self, request, telegram_id):
        """Get user by Telegram ID."""
        try:
            user = User.objects.get(telegram_id=telegram_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserStatsView(APIView):
    """Get user statistics."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current user statistics."""
        user = request.user
        bookmarks_count = Bookmark.objects.filter(user=user).count()

        stats = {
            "score": user.score,
            "total_submissions": user.total_submissions,
            "total_likes_received": user.total_likes_received,
            "bookmarks_count": bookmarks_count,
            "access_level": user.get_access_level_display(),
        }

        serializer = UserStatsSerializer(stats)
        return Response(serializer.data)
