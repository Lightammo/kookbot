import os
import sys
from dotenv import load_dotenv

load_dotenv(verbose=True)

# Bot config
BOT_ID = os.getenv("BOT_ID")
BOT_NAME = os.getenv("BOT_NAME")
BOT_NICKNAME = os.getenv("BOT_NICKNAME")
BOT_TOKEN = os.getenv("BOT_TOKEN")


# system config
ENABLE_COMPRESS = False
