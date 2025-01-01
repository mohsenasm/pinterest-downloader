import os
import logging
from datetime import datetime

from configs import WEBHOOK_BASE_URL, BOT_SECRET, BOT_ADMIN_ID

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

import glob
import random
from datetime import datetime
from pinterest_caller import download_link
from pathlib import Path
import shutil
import re
import time
from threading import Thread

logger = logging.getLogger(__name__)


class BotContainer(object):
    pass


bot_container = BotContainer()


async def create_bot():
    bot_app = (
        Application.builder().token(BOT_SECRET).updater(None).build()
    )

    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT, free_text))

    await bot_app.bot.set_webhook(url=f"{WEBHOOK_BASE_URL}/telegram", allowed_updates=Update.ALL_TYPES)

    bot_container.bot = bot_app.bot

    return bot_app


async def start(update, context):
    bot = update.get_bot()
    await log_text("start " + str(update.message.chat_id) + " " + str(update.message.from_user.username) + " " + str(update.message.chat.title), bot)


async def free_text(update, context):
    bot = update.get_bot()
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
                bot.send_document(update.message.chat_id,
                                  document=f, filename=Path(file_path).name)
        # log_text("removing after 10min: " + download_dir, bot)
        Thread(target=delyed_remove_dir, args=(10*60, download_dir)).start()


async def log_text(line, bot=None):
    try:
        if bot:
            await bot.sendMessage(BOT_ADMIN_ID, text=(str(datetime.now()) + " " + str(line)))
    except:
        pass
    with open(os.path.join(os.path.dirname(__file__), "logs.txt"), "a") as f:
        f.write(str(datetime.now()) + " " + str(line) + "\n")


def find_link(text):
    regex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
    matches = re.findall(regex, text)
    return matches[0] if len(matches) else None


def delyed_remove_dir(delay, dir):
    time.sleep(delay)
    shutil.rmtree(dir)
