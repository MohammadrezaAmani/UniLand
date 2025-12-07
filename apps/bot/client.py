"""Pyrogram client configuration with dependency injection."""
import asyncio
import logging
from typing import Optional

from django.conf import settings
from injector import inject, singleton
from pyrogram import Client
from pyrogram.enums import ParseMode

logger = logging.getLogger(__name__)


@singleton
class TelegramClient:
    """Singleton Telegram client with dependency injection."""

    @inject
    def __init__(self):
        """Initialize Pyrogram client."""
        self._client: Optional[Client] = None
        self._running = False

    def get_client(self) -> Client:
        """Get or create Pyrogram client instance."""
        if self._client is None:
            self._client = Client(
                name="uniland_bot",
                api_id=settings.TELEGRAM_API_ID,
                api_hash=settings.TELEGRAM_API_HASH,
                bot_token=settings.TELEGRAM_BOT_TOKEN,
                workdir="./bot_sessions",
                plugins=dict(root="apps.bot.plugins"),
                parse_mode=ParseMode.DEFAULT,
            )
        return self._client

    async def start(self):
        """Start the Telegram client."""
        if not self._running:
            client = self.get_client()
            await client.start()
            self._running = True
            logger.info("Telegram bot started successfully")

    async def stop(self):
        """Stop the Telegram client."""
        if self._running and self._client:
            await self._client.stop()
            self._running = False
            logger.info("Telegram bot stopped")

    def is_running(self) -> bool:
        """Check if client is running."""
        return self._running

    async def send_message(self, chat_id: int, text: str, **kwargs):
        """Send a message."""
        client = self.get_client()
        return await client.send_message(chat_id, text, **kwargs)

    async def send_document(self, chat_id: int, document: str, **kwargs):
        """Send a document."""
        client = self.get_client()
        return await client.send_document(chat_id, document, **kwargs)

    async def send_photo(self, chat_id: int, photo: str, **kwargs):
        """Send a photo."""
        client = self.get_client()
        return await client.send_photo(chat_id, photo, **kwargs)

    async def broadcast_message(self, user_ids: list, text: str, **kwargs):
        """Broadcast message to multiple users."""
        client = self.get_client()
        results = {"success": 0, "failed": 0, "errors": []}

        for user_id in user_ids:
            try:
                await client.send_message(user_id, text, **kwargs)
                results["success"] += 1
                await asyncio.sleep(0.05)  # Rate limiting
            except Exception as e:
                results["failed"] += 1
                results["errors"].append({"user_id": user_id, "error": str(e)})
                logger.error(f"Failed to send message to {user_id}: {e}")

        return results
