import os
from queue import Queue
from threading import Thread
from telegram import Bot, ParseMode
from telegram.ext import Dispatcher, MessageHandler, Updater, CommandHandler, filters
from configs import *
import pathlib, glob, random
from datetime import datetime


def start(update, context):
    bot = context.bot
    log_text("start " + str(update.message.chat_id) + " " + str(update.message.from_user.username) + " " + str(update.message.chat.title), bot)

def free_text(update, context):
    bot = context.bot
    bot.send_photo(update.message.chat_id, photo=pathlib.Path(random.choice(glob.glob("./laptop_images/*"))))
    # todo: send pin image

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
