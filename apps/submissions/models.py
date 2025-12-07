"""Submission models."""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import SoftDeleteModel, TimeStampedModel


class Submission(TimeStampedModel, SoftDeleteModel):
    """Base submission model."""

    class SubmissionType(models.TextChoices):
        DOCUMENT = "document", _("Document")
        PROFILE = "profile", _("Profile")
        MEDIA = "media", _("Media")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name=_("owner"),
    )
    submission_type = models.CharField(
        _("submission type"),
        max_length=20,
        choices=SubmissionType.choices,
        db_index=True,
    )

    is_confirmed = models.BooleanField(_("is confirmed"), default=False, db_index=True)
    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="confirmed_submissions",
        verbose_name=_("confirmed by"),
    )
    confirmed_at = models.DateTimeField(_("confirmed at"), null=True, blank=True)

    university = models.CharField(_("university"), max_length=100, default="نامشخص")
    faculty = models.CharField(_("faculty"), max_length=100, default="نامشخص")
    owner_title = models.CharField(_("owner title"), max_length=100, default="ناشناس")
    description = models.TextField(
        _("description"), default="توضیحاتی برای این محتوا ثبت نشده است."
    )

    search_text = models.TextField(_("search text"), blank=True, db_index=True)
    search_times = models.IntegerField(_("search times"), default=0)
    likes_count = models.IntegerField(_("likes count"), default=0, db_index=True)

    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Bookmark",
        related_name="bookmarks",
        verbose_name=_("liked by"),
    )

    class Meta:
        verbose_name = _("submission")
        verbose_name_plural = _("submissions")
        db_table = "submissions"
        indexes = [
            models.Index(fields=["-created_at", "is_confirmed"]),
            models.Index(fields=["submission_type", "is_confirmed"]),
            models.Index(fields=["-likes_count"]),
        ]

    def __str__(self):
        return f"{self.submission_type} #{self.id} by {self.owner}"

    def confirm(self, admin_user):
        """Confirm the submission."""
        from django.utils import timezone

        if admin_user.access_level < 2:
            raise PermissionError("User doesn't have permission to confirm submissions")

        self.is_confirmed = True
        self.confirmed_by = admin_user
        self.confirmed_at = timezone.now()
        self.update_search_text()
        self.save()

    def update_search_text(self):
        """Update search text - implemented in subclasses."""
        raise NotImplementedError("Subclasses must implement update_search_text")


class Document(Submission):
    """Document submission model."""

    class DocType(models.TextChoices):
        BOOK = "book", _("کتاب")
        PAMPHLET = "pamphlet", _("جزوه")
        EXERCISES = "exercises", _("تمرینات")
        COMPRESSED = "compressed", _("ترکیبی")
        TEMPLATE = "template", _("تمپلیت")

    file_id = models.CharField(_("file ID"), max_length=255)
    unique_id = models.CharField(_("unique ID"), max_length=255)
    file_type = models.CharField(_("file type"), max_length=20, choices=DocType.choices)
    course = models.CharField(_("course"), max_length=100)
    professor = models.CharField(_("professor"), max_length=100, default="نامشخص")
    writer = models.CharField(_("writer"), max_length=100, default="نامشخص")
    semester_year = models.IntegerField(_("semester year"), default=0)

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")
        db_table = "documents"

    def update_search_text(self):
        """Update search text for document."""
        parts = [self.get_file_type_display()]
        if self.course != "نامشخص":
            parts.append(f"درس {self.course}")
        if self.professor != "نامشخص":
            parts.append(f"استاد {self.professor}")
        if self.writer != "نامشخص":
            parts.append(f"نویسنده {self.writer}")
        if self.semester_year != 0:
            parts.append(f"سال {self.semester_year}")
        if self.faculty != "نامشخص":
            parts.append(f"دانشکده {self.faculty}")
        if self.university != "نامشخص":
            parts.append(f"دانشگاه {self.university}")
        self.search_text = " ".join(parts)

    def user_display(self):
        """Return user-friendly display text."""
        lines = [f"نوع فایل: {self.get_file_type_display()}"]
        if self.course != "نامشخص":
            lines.append(f"درس: {self.course}")
        if self.professor != "نامشخص":
            lines.append(f"استاد: {self.professor}")
        if self.faculty != "نامشخص":
            lines.append(f"دانشکده: {self.faculty}")
        if self.university != "نامشخص":
            lines.append(f"دانشگاه: {self.university}")
        if self.writer != "نامشخص":
            lines.append(f"نویسنده: {self.writer}")
        if self.semester_year != 0:
            lines.append(f"سال: {self.semester_year}")
        if self.owner_title != "ناشناس":
            lines.append(f"نام ثبت کننده: {self.owner_title}")
        lines.append(f"توضیحات:\n{self.description}")
        lines.append(f"شماره فایل: {self.id}")
        return "\n".join(lines)


class Profile(Submission):
    """Profile submission model."""

    title = models.CharField(_("title"), max_length=200)
    email = models.EmailField(_("email"), blank=True)
    phone_number = models.CharField(_("phone number"), max_length=25, blank=True)
    image_id = models.CharField(_("image ID"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
        db_table = "profiles"

    def update_search_text(self):
        """Update search text for profile."""
        parts = [f"اطلاعات {self.title}"]
        if self.faculty != "نامشخص":
            parts.append(f"دانشکده {self.faculty}")
        if self.university != "نامشخص":
            parts.append(f"دانشگاه {self.university}")
        self.search_text = " ".join(parts)

    def user_display(self):
        """Return user-friendly display text."""
        lines = [f"عنوان: {self.title}"]
        if self.email:
            lines.append(f"ایمیل: {self.email}")
        if self.phone_number:
            formatted_phone = self.phone_number[::-1].replace("+", "")
            lines.append(f"شماره تماس: {formatted_phone}")
        if self.faculty != "نامشخص":
            lines.append(f"دانشکده: {self.faculty}")
        if self.university != "نامشخص":
            lines.append(f"دانشگاه: {self.university}")
        lines.append(f"توضیحات:\n{self.description}")
        lines.append(f"شماره پروفایل: {self.id}")
        return "\n".join(lines)


class Media(Submission):
    """Media submission model."""

    url = models.URLField(_("URL"), max_length=500)
    media_type = models.CharField(_("media type"), max_length=50, blank=True)
    course = models.CharField(_("course"), max_length=100)
    professor = models.CharField(_("professor"), max_length=100)
    semester_year = models.IntegerField(_("semester year"), default=0)

    class Meta:
        verbose_name = _("media")
        verbose_name_plural = _("media")
        db_table = "media"

    def update_search_text(self):
        """Update search text for media."""
        parts = [f"فیلم درس {self.course} استاد {self.professor}"]
        if self.faculty != "نامشخص":
            parts.append(f"دانشکده {self.faculty}")
        if self.semester_year != 0:
            parts.append(f"سال {self.semester_year}")
        if self.university != "نامشخص":
            parts.append(f"دانشگاه {self.university}")
        self.search_text = " ".join(parts)

    def user_display(self):
        """Return user-friendly display text."""
        lines = [f"عنوان: {self.course} استاد {self.professor}"]
        if self.semester_year != 0:
            lines.append(f"سال: {self.semester_year}")
        if self.faculty != "نامشخص":
            lines.append(f"دانشکده: {self.faculty}")
        if self.university != "نامشخص":
            lines.append(f"دانشگاه: {self.university}")
        if self.owner_title != "ناشناس":
            lines.append(f"نام ثبت کننده: {self.owner_title}")
        lines.append(f"توضیحات:\n{self.description}")
        lines.append(f"شماره رسانه: {self.id}")
        return "\n".join(lines)


class Bookmark(TimeStampedModel):
    """Bookmark relationship model."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_bookmarks",
        verbose_name=_("user"),
    )
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name="submission_bookmarks",
        verbose_name=_("submission"),
    )

    class Meta:
        verbose_name = _("bookmark")
        verbose_name_plural = _("bookmarks")
        db_table = "bookmarks"
        unique_together = [["user", "submission"]]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["submission", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user} bookmarked {self.submission}"
