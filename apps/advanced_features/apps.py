"""Advanced features app configuration."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdvancedFeaturesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.advanced_features"
    verbose_name = _("Advanced Features")
