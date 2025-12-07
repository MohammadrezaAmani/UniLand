"""Django management command to run the Telegram bot."""
import asyncio
import logging

import uvloop
from django.core.management.base import BaseCommand

from apps.bot.client import TelegramClient
from apps.bot.di import get_injector

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run the Telegram bot"

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-uvloop",
            action="store_true",
            help="Disable uvloop for event loop",
        )

    def handle(self, *args, **options):
        """Run the bot."""
        # Install uvloop for better performance
        if not options["no_uvloop"]:
            try:
                uvloop.install()
                self.stdout.write(self.style.SUCCESS("✓ uvloop installed"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Could not install uvloop: {e}"))

        self.stdout.write(self.style.SUCCESS("Starting Telegram bot..."))

        # Get injector and client
        injector = get_injector()
        client = injector.get(TelegramClient)

        # Run the bot
        try:
            asyncio.run(self._run_bot(client))
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\nBot stopped by user"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Bot error: {e}"))
            logger.exception("Bot crashed")

    async def _run_bot(self, client: TelegramClient):
        """Async bot runner."""
        await client.start()
        self.stdout.write(self.style.SUCCESS("✓ Bot is running. Press Ctrl+C to stop."))

        # Keep the bot running
        try:
            await asyncio.Event().wait()
        finally:
            await client.stop()
