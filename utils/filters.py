import asyncio
from uniland.db import admin as admin_db
from pyrogram import filters

async def admin_check(self, client, message):
	print(message.from_user.id)
	admin = admin_db.get_admin(message.from_user.id)
	print(admin)
	print(type(admin))
	print('-'*30)
	if admin:
		return True
	return False

admin_only = filters.create(admin_check)