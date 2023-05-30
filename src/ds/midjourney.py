from __future__ import annotations

from enum import StrEnum
from uuid import UUID

from src.ds import MyBaseModel


class TriggerType(StrEnum):
    imagine = "imagine"
    upscale = "upscale"
    variation = "variati on"
    max_upscale = "max_upscale"
    reset = "reset"
    describe = "describe"
    upload = "upload"


class DrawStatus(StrEnum):
    start = "start"  # 首次触发
    generating = "generating"  # 生成中
    end = "end"  # 生成结束
    error = "error"  # 生成错误
    deleted = "deleted"  # on_message_delete
    banned = "banned"  # 提示词被禁
    verify = "verify"  # 需人工验证


class ITriggerImagine(MyBaseModel):
    prompt: str


class ITriggerUV(MyBaseModel):
    index: int
    msg_id: str
    msg_hash: str
    
    trigger_id: str  # 供业务定位触发ID，/imagine 接口返回的 trigger_id


class ITriggerReset(MyBaseModel):
    msg_id: str
    msg_hash: str
    
    trigger_id: str  # 供业务定位触发ID，/imagine 接口返回的 trigger_id


class IDraw(MyBaseModel):
    status: DrawStatus
    uuid: UUID | None
