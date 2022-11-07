import asyncio
from uniland.db import admin as admin_db
from uniland.db.db_methods import get_last_step
from uniland.utils import messages,steps
from pyrogram import filters
import pyrogram

async def admin_check(self, client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
	admin = admin_db.get_admin(message.from_user.id)
	if admin:
		return True
	return False

async def jozve_darkhast_check(self, client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
	last_step = get_last_step(message.from_user.id)
	if last_step == steps.JOZVE_DARKHAST:
		return True
	return False
async def jozve_sabt_check(self, client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
	last_step = get_last_step(message.from_user.id)
	if last_step == steps.JOZVE_SABT:
		return True
	return False
async def jozve_search_check(self, client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
	last_step = get_last_step(message.from_user.id)
	if last_step == steps.JOZVE_SEARCH:
		return True
	if message.text == 'سلام':
		return True
async def source_darkhast_check(self, client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
	last_step = get_last_step(message.from_user.id)
	if last_step == steps.SOURCE_DARKHAST:
		return True
	return False
async def source_sabt_check(self, client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
	last_step = get_last_step(message.from_user.id)
	if last_step == steps.SOURCE_SABT:
		return True
	return False
async def source_search_check(self, client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
	last_step = get_last_step(message.from_user.id)
	if last_step == steps.SOURCE_SEARCH:
		return True
	return False
async def recorded_darkhast_check(self, client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
	last_step = get_last_step(message.from_user.id)
	if last_step == steps.RECORDED_DARKHAST:
		return True
	return False
async def recorded_sabt_check(self, client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
	last_step = get_last_step(message.from_user.id)
	if last_step == steps.RECORDED_SABT:
		return True
	return False
async def recorded_search_check(self, client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
	last_step = get_last_step(message.from_user.id)
	if last_step == steps.RECORDED_SEARCH:
		return True
	

async def jozve_func_check(self, client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
	return message.text.startswith('/bo')

async def recorded_func_check(self, client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
	return message.text.startswith('/re')

async def source_func_check(self, client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
	return message.text.startswith('/so')

async def jozve_react_check(self, client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
	return message.data.startswith('like:jozve') or message.data.startswith('dislike:jozve')
async def jozve_sabt_no_check(self,  client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
	print(message.data)
	print(messages.JOZVE_SABT_NO  + ':jozve')
	return messages.JOZVE_SABT_NO  + ':jozve' == message.data
# async def recorded_search_check(self, client:pyrogram.client.Client, message:pyrogram.types.messages_and_media.message.Message):
admin_only = filters.create(admin_check)
jozve_darkhast = filters.create(jozve_darkhast_check)
jozve_sabt = filters.create(jozve_sabt_check)
jozve_search = filters.create(jozve_search_check)
source_darkhast = filters.create(source_darkhast_check)
source_sabt = filters.create(source_sabt_check)
source_search = filters.create(source_search_check)
recorded_darkhast = filters.create(recorded_darkhast_check)
recorded_sabt = filters.create(recorded_sabt_check)
recorded_search = filters.create(recorded_search_check)
jozve_check = filters.create(jozve_func_check)
recorded_check = filters.create(recorded_func_check)
source_check = filters.create(source_func_check)
jozve_react = filters.create(jozve_react_check)
jozve_sabt_no = filters.create(jozve_sabt_no_check)