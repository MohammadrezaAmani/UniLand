"""Custom filters for bot handlers."""
from pyrogram import filters

from apps.bot.di import get_injector
from apps.bot.services.user_service import UserService

injector = get_injector()
user_service = injector.get(UserService)


def user_step_filter(step: str):
    """Filter messages by user step."""
    async def func(flt, client, message):
        user_step = await user_service.get_user_step(message.from_user.id)
        return user_step == step
    
    return filters.create(func)


def access_level_filter(min_level: int = 1, max_level: int = 3):
    """Filter messages by user access level."""
    async def func(flt, client, message):
        return await user_service.check_permission(message.from_user.id, min_level)
    
    return filters.create(func)


def exact_match_filter(text: str):
    """Filter messages by exact text match."""
    async def func(flt, client, message):
        if not message.text:
            return False
        return message.text.strip() == text.strip()
    
    return filters.create(func)
