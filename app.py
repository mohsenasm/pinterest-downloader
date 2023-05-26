import os
import bot
from flask import Flask, request, send_from_directory, redirect
from telegram import Update
from configs import BOT_SECRET, PORT, WEBHOOK_BASE_URL


import os
application = Flask(__name__)

update_queue, bot_instance = bot.setup(webhook_url='{}/{}'.format(
    WEBHOOK_BASE_URL,
    BOT_SECRET
))

@application.route('/' + BOT_SECRET, methods=['GET', 'POST'])
def webhook():
    if request.json:
        update_queue.put(Update.de_json(request.get_json(force=True), bot_instance))
    return ''

@application.route('/ping/')
def ping():
    return "pong"


if __name__ == '__main__':
    host = "0.0.0.0"
    print("run application on {}:{}".format(host, PORT))
    application.run(host=host, port=PORT)
