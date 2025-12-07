"""Submission serializers."""
from rest_framework import serializers

from apps.submissions.models import Bookmark, Document, Media, Profile, Submission
from apps.users.serializers import UserSerializer


class SubmissionSerializer(serializers.ModelSerializer):
    """Base submission serializer."""

    owner = UserSerializer(read_only=True)
    confirmed_by = UserSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = [
            "id",
            "owner",
            "submission_type",
            "is_confirmed",
            "confirmed_by",
            "confirmed_at",
            "university",
            "faculty",
            "owner_title",
            "description",
            "search_text",
            "search_times",
            "likes_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "is_confirmed",
            "confirmed_by",
            "confirmed_at",
            "search_text",
            "search_times",
            "likes_count",
            "created_at",
            "updated_at",
        ]


class DocumentSerializer(SubmissionSerializer):
    """Document submission serializer."""

    class Meta(SubmissionSerializer.Meta):
        model = Document
        fields = SubmissionSerializer.Meta.fields + [
            "file_id",
            "unique_id",
            "file_type",
            "course",
            "professor",
            "writer",
            "semester_year",
        ]


class ProfileSerializer(SubmissionSerializer):
    """Profile submission serializer."""

    class Meta(SubmissionSerializer.Meta):
        model = Profile
        fields = SubmissionSerializer.Meta.fields + [
            "title",
            "email",
            "phone_number",
            "image_id",
        ]


class MediaSerializer(SubmissionSerializer):
    """Media submission serializer."""

    class Meta(SubmissionSerializer.Meta):
        model = Media
        fields = SubmissionSerializer.Meta.fields + [
            "url",
            "media_type",
            "course",
            "professor",
            "semester_year",
        ]


class BookmarkSerializer(serializers.ModelSerializer):
    """Bookmark serializer."""

    submission = SubmissionSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ["id", "submission", "created_at"]
        read_only_fields = ["id", "created_at"]
