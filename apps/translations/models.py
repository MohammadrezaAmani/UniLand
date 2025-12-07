"""Translation models for dynamic multi-language support."""
from django.db import models
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    """Supported languages."""
    
    code = models.CharField(_("language code"), max_length=10, unique=True, db_index=True)
    name = models.CharField(_("language name"), max_length=100)
    native_name = models.CharField(_("native name"), max_length=100)
    is_active = models.BooleanField(_("is active"), default=True)
    is_rtl = models.BooleanField(_("is RTL"), default=False)
    flag_emoji = models.CharField(_("flag emoji"), max_length=10, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")
        db_table = "languages"
        ordering = ["name"]
    
    def __str__(self):
        return f"{self.flag_emoji} {self.native_name} ({self.code})"


class TranslationKey(models.Model):
    """Translation keys for dynamic content."""
    
    key = models.CharField(_("key"), max_length=255, unique=True, db_index=True)
    description = models.TextField(_("description"), blank=True)
    category = models.CharField(_("category"), max_length=100, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("translation key")
        verbose_name_plural = _("translation keys")
        db_table = "translation_keys"
        ordering = ["category", "key"]
    
    def __str__(self):
        return self.key
    
    def get_translation(self, language_code: str, **kwargs) -> str:
        """Get translation for this key."""
        cache_key = f"trans:{self.key}:{language_code}"
        translation = cache.get(cache_key)
        
        if translation is None:
            try:
                trans_obj = Translation.objects.get(key=self, language__code=language_code)
                translation = trans_obj.value
                cache.set(cache_key, translation, 3600)  # Cache for 1 hour
            except Translation.DoesNotExist:
                # Fallback to English
                try:
                    trans_obj = Translation.objects.get(key=self, language__code="en")
                    translation = trans_obj.value
                except Translation.DoesNotExist:
                    translation = self.key
        
        # Format with kwargs if provided
        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except KeyError:
                pass
        
        return translation


class Translation(models.Model):
    """Actual translations for each key and language."""
    
    key = models.ForeignKey(
        TranslationKey,
        on_delete=models.CASCADE,
        related_name="translations",
        verbose_name=_("key"),
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name="translations",
        verbose_name=_("language"),
    )
    value = models.TextField(_("translation value"))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("translation")
        verbose_name_plural = _("translations")
        db_table = "translations"
        unique_together = [["key", "language"]]
        indexes = [
            models.Index(fields=["key", "language"]),
        ]
    
    def __str__(self):
        return f"{self.key.key} ({self.language.code})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Clear cache on save
        cache_key = f"trans:{self.key.key}:{self.language.code}"
        cache.delete(cache_key)


class UserLanguagePreference(models.Model):
    """User language preferences."""
    
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="language_preference",
        verbose_name=_("user"),
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        related_name="users",
        verbose_name=_("preferred language"),
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("user language preference")
        verbose_name_plural = _("user language preferences")
        db_table = "user_language_preferences"
    
    def __str__(self):
        return f"{self.user} - {self.language}"
