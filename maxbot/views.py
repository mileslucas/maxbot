import requests as r
from flask import request, redirect, render_template, url_for, abort
from maxbot import app, db
from .models import Message
from parsedatetime import Calendar
from datetime import datetime
from time import sleep, time
from numpy.random import choice
import os
import logging
from threading import Thread

logging.basicConfig(level=logging.DEBUG)

lastMessageTime = time()


@app.route("/")
def index():
    return abort(404)


@app.route("/groupme", methods=["POST"])
def groupme():
    data = request.get_json()
    logging.debug("Received message\n{}".format(data))
    if data is not None:
        logging.info("Valid message accepted")
        random_message(data)
        seconds = parse_message(data["text"])
        if seconds is not None:
            thread = messageThread(seconds)
            logging.info("Thread started")
            thread.start()
    else:
        logging.warning("Invalid message posted")
        return abort(403)
    return abort(200)


class messageThread(Thread):
    def __init__(self, delay=None):
        self.delay = delay
        return Thread.__init__(self)

    def run(self):
        logging.info("Sleeping for {} s".format(self.delay))
        sleep(self.delay)
        send_message()


LATE_MAXISMS = [
    "Look who's late again!",
    "Time's up!!! Better be on...",
    "We're all waiting for you...",
    "No more screwing around! Get on and get your game on!",
]

MAXISMS = [
    "I've never said that",
    "No, you're wrong",
    "I don't think so",
    "Probably not",
    "Nothing worse than dying",
    "But, Pochinki is my city",
    "Heyo",
]


def send_message():
    payload = {"bot_id": os.environ.get("BOT_ID"), "text": choice(LATE_MAXISMS)}
    logging.info("Sending message: {}".format(payload["text"]))
    resp = r.post(
        "https://api.groupme.com/v3/bots/post",
        params={"token": os.environ.get("TOKEN")},
        json=payload,
    )
    logging.info("Response: {}".format(resp))
    return resp


def random_message(data):
    global lastMessageTime
    like = choice([False, True], p=[0.85, 0.15])
    logging.info("Posting random message" if like else "Not posting message")
    if like and time() - lastMessageTime > int(os.getenv("MESSAGE_LIMIT")):
        payload = {"bot_id": os.environ.get("BOT_ID"), "text": choice(MAXISMS)}
        logging.info("Sending message: {}".format(payload["text"]))
        resp = r.post(
            "https://api.groupme.com/v3/bots/post",
            params={"token": os.environ.get("TOKEN")},
            json=payload,
        )
        logging.info("Response: {}".format(resp))
        lastMessageTime = time()
        return resp


def parse_message(text):
    c = Calendar()
    t_s, p_s = c.parse(text)
    time = datetime(*t_s[:6])
    td = time - datetime.now()
    return None if td.days < 0 else td.total_seconds()
