from flask import Flask
from threading import Thread
import random
import time
import requests
import logging
from uniland import usercache, search_engine

app = Flask('')

# This module is used to keep the bot alive on replit servers

@app.route('/')
def home():
  return \
      f"Total Searches: {search_engine.total_searches}<br>"\
      f"Total Users: {usercache.total_users}<br>" \
      f"Amount of confirmed Submissions: {search_engine.total_confirmed_subs}<br>" \


def run():
  app.run(host='0.0.0.0', port=8080)


def ping(target, debug):
  while (True):
    r = requests.get(target)
    if (debug == True):
      print("Status Code: " + str(r.status_code))
    time.sleep(random.randint(
        180, 300))  # alternate ping time between 3 and 5 minutes


def awake(target, debug=False):
  log = logging.getLogger('werkzeug')
  log.disabled = True
  app.logger.disabled = True
  t = Thread(target=run)
  r = Thread(target=ping, args=(
      target,
      debug,
  ))
  t.start()
  r.start()
