from __future__ import annotations

from typing import MutableMapping

from aiohttp import hdrs

from src.ds import TriggerID, MyBaseModel
from src.ds.discord import ICallback, TriggerStatus


class ITrigger(MyBaseModel):
    id: TriggerID
    status: TriggerStatus


class FetchMethod:
    get = hdrs.METH_GET
    post = hdrs.METH_POST


class TriggerImagineIn(MyBaseModel):
    prompt: str


class TriggerUVIn(MyBaseModel):
    index: int
    msg_id: str
    msg_hash: str
    
    trigger_id: str  # 供业务定位触发ID，/imagine 接口返回的 trigger_id


class TriggerResetIn(MyBaseModel):
    msg_id: str
    msg_hash: str
    
    trigger_id: str  # 供业务定位触发ID，/imagine 接口返回的 trigger_id


ITriggerManager = MutableMapping[TriggerID, ICallback]
