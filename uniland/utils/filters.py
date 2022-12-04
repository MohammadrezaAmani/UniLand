import asyncio
from uniland import usercache
from uniland.db.tables import User
from uniland.utils import messages, steps
from pyrogram import filters
import pyrogram


def access_level(min: int = 1, max: int = 3):
    async def func(self, client, message):
        return usercache.has_permission(
            message.from_user.id, min_permission=min, max_permission=max
        )

    return filters.create(func)


def user_step(step: str):
    async def func(self, client, message):
        return usercache.match_step(message.from_user.id, step)

    return filters.create(func)

def exact_match(txt: str):
    async def func(self, client, message):
        if message.text is None:
            return False
        return message.text.strip() == txt.strip()

    return filters.create(func)
