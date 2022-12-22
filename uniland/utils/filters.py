from uniland import usercache
from pyrogram import filters
from pyrogram.enums import ChatType


def access_level(min: int = 1, max: int = 3):
    async def func(self, client, message):
        return usercache.has_permission(
            message.from_user.id, min_permission=min, max_permission=max
        )

    return filters.create(func)


def user_step(step: str):
    async def func(self, client, message):
        if message.chat.type != ChatType.PRIVATE:
            return False
        return usercache.match_step(message.from_user.id, step)

    return filters.create(func)


async def user_existence_check(self, client, message):
    return usercache.has_user(message.from_user.id)


user_exists = filters.create(user_existence_check)


def exact_match(txt: str):
    async def func(self, client, message):
        if message.text is None:
            return False
        return message.text.strip() == txt.strip()

    return filters.create(func)
