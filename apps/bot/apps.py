"""Bot app configuration."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.bot"
    verbose_name = _("Telegram Bot")
