from typing import Dict

from src.ds import TriggerID
from src.ds.server import ITriggerManager

TEMP_MAP: Dict[TriggerID, bool] = {}  # 临时存储消息流转信息


def get_temp(trigger_id: TriggerID):
    return TEMP_MAP.get(trigger_id)


def set_temp(trigger_id: TriggerID):
    TEMP_MAP[trigger_id] = True


def pop_temp(trigger_id: TriggerID):
    try:
        TEMP_MAP.pop(trigger_id)
    except KeyError:
        pass


trigger_manager: ITriggerManager = {}
