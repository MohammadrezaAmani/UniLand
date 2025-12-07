"""Translation service for dynamic multi-language support."""
import logging

from asgiref.sync import sync_to_async
from django.core.cache import cache

from apps.translations.models import Language, TranslationKey

logger = logging.getLogger(__name__)


class TranslationService:
    """Service for handling translations."""
    
    CACHE_TTL = 3600  # 1 hour
    
    @sync_to_async
    def get_translation(self, key: str, language_code: str = "en", **kwargs) -> str:
        """Get translation for a key in specified language."""
        cache_key = f"trans:{key}:{language_code}"
        translation = cache.get(cache_key)
        
        if translation is None:
            try:
                trans_key = TranslationKey.objects.get(key=key)
                translation = trans_key.get_translation(language_code, **kwargs)
                cache.set(cache_key, translation, self.CACHE_TTL)
            except TranslationKey.DoesNotExist:
                logger.warning(f"Translation key not found: {key}")
                translation = key
        
        # Format with kwargs
        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except (KeyError, ValueError) as e:
                logger.error(f"Error formatting translation {key}: {e}")
        
        return translation
    
    @sync_to_async
    def get_user_language(self, user_id: int) -> str:
        """Get user's preferred language code."""
        from apps.users.models import User
        
        cache_key = f"user_lang:{user_id}"
        lang_code = cache.get(cache_key)
        
        if lang_code is None:
            try:
                user = User.objects.select_related("language_preference__language").get(
                    telegram_id=user_id
                )
                if hasattr(user, "language_preference") and user.language_preference.language:
                    lang_code = user.language_preference.language.code
                else:
                    lang_code = user.language_code or "en"
                
                cache.set(cache_key, lang_code, self.CACHE_TTL)
            except User.DoesNotExist:
                lang_code = "en"
        
        return lang_code
    
    @sync_to_async
    def set_user_language(self, user_id: int, language_code: str) -> bool:
        """Set user's preferred language."""
        from apps.users.models import User
        from apps.translations.models import UserLanguagePreference
        
        try:
            user = User.objects.get(telegram_id=user_id)
            language = Language.objects.get(code=language_code, is_active=True)
            
            pref, created = UserLanguagePreference.objects.get_or_create(user=user)
            pref.language = language
            pref.save()
            
            # Update user's language_code field
            user.language_code = language_code
            user.save(update_fields=["language_code"])
            
            # Clear cache
            cache.delete(f"user_lang:{user_id}")
            
            return True
        except (User.DoesNotExist, Language.DoesNotExist) as e:
            logger.error(f"Error setting user language: {e}")
            return False
    
    @sync_to_async
    def get_available_languages(self):
        """Get list of available languages."""
        cache_key = "available_languages"
        languages = cache.get(cache_key)
        
        if languages is None:
            languages = list(
                Language.objects.filter(is_active=True).values(
                    "code", "name", "native_name", "flag_emoji", "is_rtl"
                )
            )
            cache.set(cache_key, languages, self.CACHE_TTL)
        
        return languages
    
    async def t(self, key: str, lang: str = "en", **kwargs) -> str:
        """Shorthand for get_translation."""
        return await self.get_translation(key, lang, **kwargs)


# Global instance
translation_service = TranslationService()
