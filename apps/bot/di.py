"""Dependency injection configuration."""
from injector import Injector, Module, provider, singleton

from apps.bot.client import TelegramClient
from apps.bot.services.user_service import UserService
from apps.bot.services.submission_service import SubmissionService
from apps.search.services import SearchService


class BotModule(Module):
    """Bot dependency injection module."""

    @singleton
    @provider
    def provide_telegram_client(self) -> TelegramClient:
        """Provide Telegram client singleton."""
        return TelegramClient()

    @singleton
    @provider
    def provide_user_service(self) -> UserService:
        """Provide user service singleton."""
        return UserService()

    @singleton
    @provider
    def provide_submission_service(self) -> SubmissionService:
        """Provide submission service singleton."""
        return SubmissionService()

    @singleton
    @provider
    def provide_search_service(self) -> SearchService:
        """Provide search service singleton."""
        return SearchService()


_injector = None


def get_injector() -> Injector:
    """Get or create the global injector instance."""
    global _injector
    if _injector is None:
        _injector = Injector([BotModule()])
    return _injector
