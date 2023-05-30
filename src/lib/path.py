import os
import pathlib

import settings_discord


def ensure_exist(dir: pathlib.Path):
    if not dir.exists():
        os.mkdir(dir)
    return dir


PATH_PATH = pathlib.Path(__file__)
LIB_DIR = PATH_PATH.parent
SRC_DIR = LIB_DIR.parent
PROJECT_DIR = SRC_DIR.parent
DATA_DIR = ensure_exist(PROJECT_DIR / "data")
BANNED_WORDS_FILE_PATH = PROJECT_DIR / settings_discord.BANNED_WORDS_RELATIVE_FILE_PATH
