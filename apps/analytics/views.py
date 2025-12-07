"""Analytics API views."""
from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.submissions.models import Submission
from apps.users.models import User


class StatisticsView(APIView):
    """Get bot statistics."""

    permission_classes = [IsAdminUser]

    def get(self, request):
        """Get comprehensive statistics."""
        now = timezone.now()

        stats = {
            "users": {
                "total": User.objects.count(),
                "active_1h": User.objects.filter(last_active__gte=now - timedelta(hours=1)).count(),
                "active_24h": User.objects.filter(last_active__gte=now - timedelta(hours=24)).count(),
                "active_7d": User.objects.filter(last_active__gte=now - timedelta(days=7)).count(),
                "new_1h": User.objects.filter(signup_date__gte=now - timedelta(hours=1)).count(),
                "new_24h": User.objects.filter(signup_date__gte=now - timedelta(hours=24)).count(),
                "new_7d": User.objects.filter(signup_date__gte=now - timedelta(days=7)).count(),
                "admins": User.objects.filter(access_level=User.AccessLevel.ADMIN).count(),
                "editors": User.objects.filter(access_level=User.AccessLevel.EDITOR).count(),
            },
            "submissions": {
                "total": Submission.objects.count(),
                "confirmed": Submission.objects.filter(is_confirmed=True).count(),
                "pending": Submission.objects.filter(is_confirmed=False, is_deleted=False).count(),
                "by_type": dict(
                    Submission.objects.values("submission_type").annotate(count=Count("id"))
                ),
            },
        }

        return Response(stats)


class LeaderboardView(APIView):
    """Get user leaderboard."""

    def get(self, request):
        """Get top users by score."""
        limit = int(request.query_params.get("limit", 10))

        top_users = User.objects.filter(is_active=True).order_by("-score")[:limit]

        leaderboard = [
            {
                "rank": idx + 1,
                "telegram_id": user.telegram_id,
                "username": user.username,
                "full_name": user.full_name,
                "score": user.score,
                "submissions": user.total_submissions,
                "likes": user.total_likes_received,
            }
            for idx, user in enumerate(top_users)
        ]

        return Response({"leaderboard": leaderboard})
