import os
import pathlib
from os import getenv

from dotenv import load_dotenv

from src.lib.exceptions import MissRequiredVariable

load_dotenv()


# ----------------------------
# path
# ----------------------------


def ensure_exist(dir: pathlib.Path):
    if not dir.exists():
        os.mkdir(dir)
    return dir


SETTINGS_PATH = pathlib.Path(__file__)
PROJECT_DIR = SETTINGS_PATH.parent
SRC_DIR = PROJECT_DIR / "src"
DATA_DIR = ensure_exist(PROJECT_DIR / "data")

# ----------------------------
# fastapi
# ----------------------------


API_PREFIX = "/v1"
UVICORN_RELOAD_ENABLED = True

# ----------------------------
# discord
# ----------------------------

DISCORD_EMBED_IN_FASTAPI_ENABLED = True  # 把discord运行在fastapi内部

DISCORD_GUILD_ID = getenv("GUILD_ID")
DISCORD_CHANNEL_ID = getenv("CHANNEL_ID")
DISCORD_USER_TOKEN = getenv("USER_TOKEN")
DISCORD_BOT_TOKEN = getenv("BOT_TOKEN")

if not all([DISCORD_GUILD_ID, DISCORD_CHANNEL_ID, DISCORD_USER_TOKEN, DISCORD_BOT_TOKEN]):
    raise MissRequiredVariable("Missing required environment variable: [GUILD_ID, CHANNEL_ID, USER_TOKEN, BOT_TOKEN]")

DISCORD_WEBSOCKET_ENABLED = False
DISCORD_DUMP_CALLBACK_DATA = True
DISCORD_CALLBACK_URL = getenv("CALLBACK_URL")  # todo: enable without it

DISCORD_TRIGGER_URL = "https://discord.com/api/v9/interactions"
DISCORD_UPLOAD_URL = f"https://discord.com/api/v9/channels/{DISCORD_CHANNEL_ID}/attachments"

DISCORD_PROMPT_PREFIX = "<#"
DISCORD_PROMPT_SUFFIX = "#>"
DISCORD_TRIGGER_ID_PATTERN = f"{DISCORD_PROMPT_PREFIX}(\w+?){DISCORD_PROMPT_SUFFIX}"  # 消息 ID 正则

# ----------------------------
# midjourney
# ----------------------------


MIDJOURNEY_BANNED_WORDS_FILE_PATH = PROJECT_DIR / "banned_words.txt"
MIDJOURNEY_BOT_ID = 936929561302675456
