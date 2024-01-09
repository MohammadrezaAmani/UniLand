from pyrogram import filters
from pyrogram.enums import ChatType

from uniland import usercache


def access_level(min: int = 1, max: int = 3):
    """
    Check if the user has the required access level.

    Args:
        min (int, optional): The minimum access level required. Defaults to 1.
        max (int, optional): The maximum access level required. Defaults to 3.

    Returns:
        bool: True if the user has the required access level, False otherwise.
    """

    async def func(self, client, message):
        return usercache.has_permission(
            message.from_user.id, min_permission=min, max_permission=max
        )

    return filters.create(func)


def user_step(step: str):
    """
    Check if the user's current step matches the given step.

    Args:
        step (str): The step to match.

    Returns:
        bool: True if the user's current step matches the given step, False otherwise.
    """

    async def func(self, client, message):
        if message.chat.type != ChatType.PRIVATE:
            return False
        return usercache.match_step(message.from_user.id, step)

    return filters.create(func)


async def user_existence_check(self, client, message):
    """
    Check if a user exists in the user cache.

    Args:
        client (TelegramClient): The Telegram client.
        message (Message): The message object.

    Returns:
        bool: True if the user exists in the cache, False otherwise.
    """
    try:
        return usercache.has_user(message.from_user.id)
    except:
        return False


user_exists = filters.create(user_existence_check)


def exact_match(txt: str):
    """
    Check if the message text is an exact match to the given text.

    Args:
        txt (str): The text to match against.

    Returns:
        Callable: A filter function that checks if the message text is an exact match.
    """

    async def func(self, client, message):
        if message.text is None:
            return False
        return message.text.strip() == txt.strip()

    return filters.create(func)
