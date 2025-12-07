"""User serializers."""
from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    full_name = serializers.CharField(read_only=True)
    access_level_display = serializers.CharField(source="get_access_level_display", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "telegram_id",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "language_code",
            "access_level",
            "access_level_display",
            "last_step",
            "is_active",
            "is_banned",
            "last_active",
            "signup_date",
            "total_submissions",
            "total_likes_received",
            "score",
        ]
        read_only_fields = [
            "id",
            "telegram_id",
            "last_active",
            "signup_date",
            "total_submissions",
            "total_likes_received",
            "score",
        ]


class UserStatsSerializer(serializers.Serializer):
    """User statistics serializer."""

    score = serializers.IntegerField()
    total_submissions = serializers.IntegerField()
    total_likes_received = serializers.IntegerField()
    bookmarks_count = serializers.IntegerField()
    access_level = serializers.CharField()
