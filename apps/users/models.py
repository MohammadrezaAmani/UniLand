"""User models."""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class UserManager(BaseUserManager):
    """Custom user manager."""

    def create_user(self, telegram_id, **extra_fields):
        """Create and save a regular user."""
        if not telegram_id:
            raise ValueError(_("The Telegram ID must be set"))
        user = self.model(telegram_id=telegram_id, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, **extra_fields):
        """Create and save a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("access_level", User.AccessLevel.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(telegram_id, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """Custom user model using Telegram ID as primary identifier."""

    class AccessLevel(models.IntegerChoices):
        ORDINARY = 1, _("Ordinary")
        EDITOR = 2, _("Editor")
        ADMIN = 3, _("Admin")

    telegram_id = models.BigIntegerField(_("telegram ID"), unique=True, db_index=True)
    username = models.CharField(_("username"), max_length=255, blank=True, null=True)
    first_name = models.CharField(_("first name"), max_length=255, blank=True)
    last_name = models.CharField(_("last name"), max_length=255, blank=True)
    language_code = models.CharField(_("language code"), max_length=10, default="fa")

    access_level = models.IntegerField(
        _("access level"),
        choices=AccessLevel.choices,
        default=AccessLevel.ORDINARY,
        db_index=True,
    )
    last_step = models.CharField(_("last step"), max_length=100, default="start_stage")

    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_banned = models.BooleanField(_("banned"), default=False, db_index=True)

    last_active = models.DateTimeField(_("last active"), default=timezone.now, db_index=True)
    signup_date = models.DateTimeField(_("signup date"), auto_now_add=True)

    # Statistics
    total_submissions = models.IntegerField(_("total submissions"), default=0)
    total_likes_received = models.IntegerField(_("total likes received"), default=0)
    score = models.IntegerField(_("score"), default=0, db_index=True)

    objects = UserManager()

    USERNAME_FIELD = "telegram_id"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "users"
        indexes = [
            models.Index(fields=["-score"]),
            models.Index(fields=["-last_active"]),
            models.Index(fields=["access_level", "-score"]),
        ]

    def __str__(self):
        return f"@{self.username}" if self.username else f"User {self.telegram_id}"

    @property
    def full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or str(self.telegram_id)

    def update_activity(self):
        """Update last active timestamp."""
        self.last_active = timezone.now()
        self.save(update_fields=["last_active"])

    def update_score(self):
        """Calculate and update user score."""
        self.score = (self.total_submissions * 5) + self.total_likes_received
        self.save(update_fields=["score"])

    def has_permission(self, min_level=AccessLevel.ORDINARY):
        """Check if user has minimum permission level."""
        return self.access_level >= min_level and not self.is_banned
