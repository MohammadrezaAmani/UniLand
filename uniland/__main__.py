import asyncio

try:
  import uvloop
except:
  print("uvloop is not installed")

from pyrogram import Client
from .config import API_ID, API_HASH, BOT_TOKEN, REPL_URL
from .utils import keep_alive

if __name__ == "__main__":

  # on_repl = True if "y" in input("Are you running this on repl.it? (y/n): ").lower() else False
  on_repl = True

  if on_repl:
    keep_alive.awake(REPL_URL, False)

  plugins = dict(
    root="uniland.plugins",
    include=[
      # Test plugin for testing functionalities
      "fortest",
      # 'uniland.plugins.start folder'
      "start.start",
      # 'uniland.plugins.submission folder'
      "submission.choose",
      "submission.document",
      "submission.media",
      "submission.profile",
      "submission.submission",
      # 'uniland.plugins.search folder'
      "search.inlinesearch",
      "search.pvsearch",
      # 'uniland.plugins.admin folder'
      "admin.admin_panel",
      "admin.access",
      "admin.edit",
      "admin.confirmation",
      # 'uniland.plugins.navigation folder'
      "navigation.back_handler",
      # 'uniland.plugins.dashboard folder'
      "dashboard.myprofile",
      "dashboard.help",
    ],
  )

  try:
    uvloop.install()
  except:
    print("Could not apply uvloop on project")

  Client(
    "UniLand",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=plugins,
  ).run()
