"""Load translations from JSON files."""
import json
import logging
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.translations.models import Language, Translation, TranslationKey

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load translations from JSON files"
    
    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            help="Path to translations JSON file",
            default="translations.json",
        )
    
    def handle(self, *args, **options):
        file_path = Path(options["file"])
        
        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return
        
        self.stdout.write(self.style.SUCCESS(f"Loading translations from {file_path}..."))
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        with transaction.atomic():
            # Load languages
            for lang_data in data.get("languages", []):
                language, created = Language.objects.get_or_create(
                    code=lang_data["code"],
                    defaults={
                        "name": lang_data["name"],
                        "native_name": lang_data["native_name"],
                        "is_rtl": lang_data.get("is_rtl", False),
                        "flag_emoji": lang_data.get("flag_emoji", ""),
                        "is_active": lang_data.get("is_active", True),
                    },
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"  Created language: {language}")
                    )
            
            # Load translations
            translations_data = data.get("translations", {})
            total = 0
            
            for category, keys in translations_data.items():
                for key, translations in keys.items():
                    # Create or get translation key
                    trans_key, created = TranslationKey.objects.get_or_create(
                        key=key,
                        defaults={
                            "category": category,
                            "description": translations.get("description", ""),
                        },
                    )
                    
                    # Create translations for each language
                    for lang_code, value in translations.items():
                        if lang_code in ["description"]:
                            continue
                        
                        try:
                            language = Language.objects.get(code=lang_code)
                            Translation.objects.update_or_create(
                                key=trans_key,
                                language=language,
                                defaults={"value": value},
                            )
                            total += 1
                        except Language.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"  Language not found: {lang_code}"
                                )
                            )
        
        self.stdout.write(
            self.style.SUCCESS(f"✅ Loaded {total} translations successfully!")
        )
