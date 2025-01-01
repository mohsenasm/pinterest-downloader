import os
from dotenv import load_dotenv

if os.path.isfile("secret.env"):
    print("loading envs from secret.env")
    load_dotenv("secret.env")

BOT_ADMIN_ID = os.environ['BOT_ADMIN_ID']
BOT_SECRET = os.environ['BOT_SECRET']
PORT = os.environ['PORT']
WEBHOOK_BASE_URL = os.environ['WEBHOOK_BASE_URL']
LOG_VIEWER_USERNAME = os.environ['LOG_VIEWER_USERNAME']
LOG_VIEWER_PASSWORD = os.environ['LOG_VIEWER_PASSWORD']