import os
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, MessageHandler, Updater, CommandHandler, filters
from configs import *
import glob, random
from datetime import datetime
from pinterest_caller import download_link
from pathlib import Path
import shutil
import re

def start(update, context):
    bot = context.bot
    log_text("start " + str(update.message.chat_id) + " " + str(update.message.from_user.username) + " " + str(update.message.chat.title), bot)

def find_link(text):
    regex=ur"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
    matches = re.findall(regex, text)
    return matches[0] if len(matches) else None

def free_text(update, context):
    bot = context.bot
    laptop_image_path = random.choice(glob.glob("./laptop_images/*"))
    with open(laptop_image_path, 'rb') as f:
        bot.send_sticker(update.message.chat_id, f)
    link = find_link(update.message.text)
    if link:
        file_paths, download_dir = download_link(link)
        # log_text("file_paths: " + str(file_paths), bot)
        for file_path in file_paths:
            # log_text("sending: " + str(file_path), bot)
            with open(file_path, 'rb') as f:
                bot.send_document(update.message.chat_id, document=f, filename=Path(file_path).name)
        # log_text("removing: " + download_dir, bot)
        shutil.rmtree(download_dir)
        # log_text("removed: " + download_dir, bot)

def echo(update, context):
    bot = context.bot
    bot.sendMessage(update.message.chat_id, text=update.message.text)

def error(update, context):
    bot = context.bot
    log_text('error update: "%s" caused error: "%s"' % (update, context.error), bot)

def log_text(line, bot=None):
    try:
        if bot:
            bot.sendMessage(BOT_ADMIN_ID, text=(str(datetime.now()) + " " + str(line)))
    except:
        pass
    with open(os.path.join(os.path.dirname(__file__),"logs.txt"), "a") as f:
        f.write(str(datetime.now()) + " " + str(line) + "\n")


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    if webhook_url:
        bot = Bot(BOT_SECRET)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(BOT_SECRET)
        bot = updater.bot
        dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.Filters.text | filters.Filters.command, free_text))
    log_text("start the bot")

    # log all errors
    dp.add_error_handler(error)
    if webhook_url:
        bot.set_webhook(url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()
