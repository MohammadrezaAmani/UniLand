"""Submission API views."""
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.pagination import StandardResultsSetPagination
from apps.submissions.models import Submission
from apps.submissions.serializers import SubmissionSerializer


class SubmissionListView(generics.ListAPIView):
    """List all confirmed submissions."""

    serializer_class = SubmissionSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get confirmed submissions."""
        return Submission.objects.filter(
            is_confirmed=True,
            is_deleted=False,
        ).select_related("owner", "confirmed_by").order_by("-created_at")


class SubmissionDetailView(generics.RetrieveAPIView):
    """Get submission details."""

    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Submission.objects.select_related("owner", "confirmed_by")


class PendingSubmissionsView(generics.ListAPIView):
    """List pending submissions (admin only)."""

    serializer_class = SubmissionSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get pending submissions."""
        if self.request.user.access_level < 2:
            return Submission.objects.none()

        return Submission.objects.filter(
            is_confirmed=False,
            is_deleted=False,
        ).select_related("owner").order_by("-created_at")


class ConfirmSubmissionView(APIView):
    """Confirm a submission (admin only)."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Confirm submission."""
        if request.user.access_level < 2:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            submission = Submission.objects.get(pk=pk)
            submission.confirm(request.user)
            serializer = SubmissionSerializer(submission)
            return Response(serializer.data)
        except Submission.DoesNotExist:
            return Response(
                {"error": "Submission not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except PermissionError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN,
            )


class RejectSubmissionView(APIView):
    """Reject a submission (admin only)."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Reject submission."""
        if request.user.access_level < 2:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        reason = request.data.get("reason", "No reason provided")

        try:
            submission = Submission.objects.get(pk=pk)
            submission.soft_delete()

            # TODO: Send notification to user about rejection

            return Response({"message": "Submission rejected"})
        except Submission.DoesNotExist:
            return Response(
                {"error": "Submission not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
