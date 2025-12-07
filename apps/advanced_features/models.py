"""Advanced feature models."""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class Notification(TimeStampedModel):
    """User notifications."""
    
    class NotificationType(models.TextChoices):
        SUBMISSION_CONFIRMED = "submission_confirmed", _("Submission Confirmed")
        SUBMISSION_REJECTED = "submission_rejected", _("Submission Rejected")
        NEW_LIKE = "new_like", _("New Like")
        NEW_COMMENT = "new_comment", _("New Comment")
        SYSTEM = "system", _("System")
        BROADCAST = "broadcast", _("Broadcast")
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    type = models.CharField(max_length=50, choices=NotificationType.choices)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["user", "is_read"]),
        ]


class UserActivity(TimeStampedModel):
    """Track user activities."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    action = models.CharField(max_length=100, db_index=True)
    details = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        db_table = "user_activities"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["action", "-created_at"]),
        ]


class AIRecommendation(TimeStampedModel):
    """AI-powered recommendations."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recommendations",
    )
    submission = models.ForeignKey(
        "submissions.Submission",
        on_delete=models.CASCADE,
        related_name="recommendations",
    )
    score = models.FloatField(default=0.0)
    reason = models.TextField(blank=True)
    is_shown = models.BooleanField(default=False)
    is_clicked = models.BooleanField(default=False)
    
    class Meta:
        db_table = "ai_recommendations"
        ordering = ["-score", "-created_at"]
        unique_together = [["user", "submission"]]


class UserBadge(TimeStampedModel):
    """User achievement badges."""
    
    class BadgeType(models.TextChoices):
        CONTRIBUTOR = "contributor", _("Contributor")
        TOP_UPLOADER = "top_uploader", _("Top Uploader")
        POPULAR = "popular", _("Popular")
        VERIFIED = "verified", _("Verified")
        EARLY_ADOPTER = "early_adopter", _("Early Adopter")
        HELPFUL = "helpful", _("Helpful")
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="badges",
    )
    badge_type = models.CharField(max_length=50, choices=BadgeType.choices)
    level = models.IntegerField(default=1)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "user_badges"
        unique_together = [["user", "badge_type"]]


class ScheduledMessage(TimeStampedModel):
    """Scheduled messages for users."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="scheduled_messages",
    )
    message = models.TextField()
    scheduled_for = models.DateTimeField(db_index=True)
    is_sent = models.BooleanField(default=False, db_index=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = "scheduled_messages"
        ordering = ["scheduled_for"]


class UserSubscription(TimeStampedModel):
    """User subscriptions to topics/tags."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    topic = models.CharField(max_length=100, db_index=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "user_subscriptions"
        unique_together = [["user", "topic"]]


class ContentReport(TimeStampedModel):
    """User reports for inappropriate content."""
    
    class ReportReason(models.TextChoices):
        SPAM = "spam", _("Spam")
        INAPPROPRIATE = "inappropriate", _("Inappropriate")
        COPYRIGHT = "copyright", _("Copyright Violation")
        MISLEADING = "misleading", _("Misleading")
        OTHER = "other", _("Other")
    
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports_made",
    )
    submission = models.ForeignKey(
        "submissions.Submission",
        on_delete=models.CASCADE,
        related_name="reports",
    )
    reason = models.CharField(max_length=50, choices=ReportReason.choices)
    description = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False, db_index=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports_resolved",
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = "content_reports"
        ordering = ["-created_at"]


class UserSession(TimeStampedModel):
    """Track user sessions."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    session_id = models.CharField(max_length=255, unique=True, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    last_activity = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = "user_sessions"
        ordering = ["-created_at"]


class FeatureFlag(models.Model):
    """Feature flags for A/B testing and gradual rollouts."""
    
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)
    is_enabled = models.BooleanField(default=False)
    rollout_percentage = models.IntegerField(default=0)  # 0-100
    enabled_for_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="enabled_features",
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "feature_flags"
    
    def is_enabled_for_user(self, user):
        """Check if feature is enabled for specific user."""
        if not self.is_enabled:
            return False
        
        if self.enabled_for_users.filter(id=user.id).exists():
            return True
        
        # Check rollout percentage
        if self.rollout_percentage >= 100:
            return True
        
        if self.rollout_percentage <= 0:
            return False
        
        # Use user ID for consistent rollout
        return (user.id % 100) < self.rollout_percentage
