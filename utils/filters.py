import asyncio
from uniland.db import admin as admin_db
from uniland.utils import messages
from pyrogram import filters

async def admin_check(self, client, message):
	admin = admin_db.get_admin(message.from_user.id)
	if admin:
		return True
	return False

admin_only = filters.create(admin_check)