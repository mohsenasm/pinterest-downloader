import os
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, MessageHandler, Updater, CommandHandler, filters
from configs import *
import glob, random
from datetime import datetime
from pinterest_caller import download_link

def start(update, context):
    bot = context.bot
    log_text("start " + str(update.message.chat_id) + " " + str(update.message.from_user.username) + " " + str(update.message.chat.title), bot)

def free_text(update, context):
    bot = context.bot
    laptop_image_path = random.choice(glob.glob("./laptop_images/*"))
    with open(laptop_image_path, 'rb') as f:
        bot.send_sticker(update.message.chat_id, f)
    files, download_dir = download_link(update.message.text)
    for file in files:
        log_text("sending: " + str(file), bot)
        with open(file, 'rb') as f:
            bot.send_document(update.message.chat_id, f)
    log_text("removing: " + download_dir, bot)
    os.rmdir(download_dir)
    log_text("removed: " + download_dir, bot)

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
