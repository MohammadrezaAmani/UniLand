import logging
import random
import time
from threading import Thread

import requests
from flask import Flask

from uniland import search_engine, usercache

app = Flask("")

# This module is used to keep the bot alive on replit servers


@app.route("/")
def home():
    """
    This function returns a string representing the home page of a Python program.

    Returns:
        str: A message indicating that the home page has been found.
    """
    return "You have found the home of a Python program!"


@app.route("/stats")
def stats():
    return (
        f"Total Searches: {search_engine.total_searches}<br>"
        f"Total Users: {usercache.total_users}<br>"
        f"Total confirmed Submissions: {search_engine.total_confirmed_subs}<br>"
    )


def run(host: str = "0.0.0.0", port: int = 8080):
    """
    Runs the application on the specified host and port.

    Args:
        host (str): The host IP address to bind the application to. Default is "0.0.0.0".
        port (int): The port number to run the application on. Default is 8080.
    """
    app.run(host=host, port=port)


def ping(target, debug):
    """
    Sends a GET request to the specified target URL at regular intervals.

    Args:
        target (str): The URL to send the GET request to.
        debug (bool): If True, prints the status code of the response.

    Returns:
        None
    """
    while True:
        r = requests.get(target)
        if debug is True:
            print("Status Code: " + str(r.status_code))
        time.sleep(
            random.randint(180, 300)
        )  # alternate ping time between 3 and 5 minutes


def awake(target, debug=False):
    """
    Starts a background thread to keep the application alive.

    Args:
        target (callable): The target function to be executed in the background thread.
        debug (bool, optional): Whether to enable debug mode. Defaults to False.
    """
    log = logging.getLogger("werkzeug")
    log.disabled = True
    app.logger.disabled = True
    t = Thread(target=run)
    r = Thread(
        target=ping,
        args=(
            target,
            debug,
        ),
    )
    t.start()
    r.start()
