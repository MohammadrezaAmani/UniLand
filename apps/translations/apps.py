"""Translations app configuration."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TranslationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.translations"
    verbose_name = _("Translations")
