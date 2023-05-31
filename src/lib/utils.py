import hashlib
import re
import time

from fastapi import HTTPException

import settings
from src.ds import TriggerID
from src.lib.log import logger


def get_trigger_id(content: str) -> TriggerID:
    match = re.findall(settings.DISCORD_TRIGGER_ID_PATTERN, content)
    try:
        return int(match[0])
    except Exception as e:
        logger.debug(e)
        raise HTTPException(500, e.__str__())


def unique_id():
    """生成唯一的 10 位数字，作为任务 ID"""
    return int(hashlib.sha256(str(time.time()).encode("utf-8")).hexdigest(), 16) % 10 ** 10
