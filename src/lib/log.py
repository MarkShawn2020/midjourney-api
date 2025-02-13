import sys
from os import getenv

from loguru import logger as _logger

logger = _logger

# logger config
_lvl = getenv("LOG_LEVEL", default="ERROR")
_format = '<green>{time:%Y-%m-%d %H:%M:%S}</> | ' + \
          '<level>{level}</> | ' + \
          '{process.id}-{thread.id} | ' + \
          '"{file.path}:{line}":<blue>{function}</> ' + \
          '- <level>{message}</>'
logger.remove()
logger.add(
    sys.stdout, level=_lvl, format=_format, colorize=True,
)

logger.add(
    f"log/mj-api.log",
    level=_lvl,
    format=_format,
    rotation="00:00",
    retention="3 days",
    backtrace=True,
    diagnose=True,
    enqueue=True
)
