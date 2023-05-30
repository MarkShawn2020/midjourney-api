from __future__ import annotations

from enum import StrEnum
from typing import List

# from discord.types.message import Attachment
from discord.types.snowflake import Snowflake

from src.ds import TriggerID, MyBaseModel


class TriggerType(StrEnum):
    imagine = "imagine"
    upscale = "upscale"
    variation = "variation"
    max_upscale = "max_upscale"
    reset = "reset"
    describe = "describe"
    upload = "upload"


class TriggerStatus(StrEnum):
    # when trigger
    success = "success"
    fail = "fail"
    
    # when discord return
    message = "message"
    edit = "editing"
    delete = "delete"
    
    # others
    start = "start"  # 首次触发
    generating = "generating"  # 生成中
    end = "end"  # 生成结束
    error = "error"  # 生成错误
    banned = "banned"  # 提示词被禁
    
    verify = "verify"  # 需人工验证
    
    unknown = "unknown"  # fallback for test


class IAttachment(MyBaseModel):
    """
    不要直接用 discord.types.message.Attachment(TypedDict)
        - 会导致 circular import（官方 discord issues 里搜索也无果：https://github.com/Rapptz/discord.py/issues?q=is%3Aissue+circular）
        - 在 fastapi router 里即使声明 data 为 TypedDict，也会自动转成 BaseModel 进行校验，
            而 pydantic v1 是不支持 NotRequired 字段校验的（会默认 Required），导致bug
    因此最好的办法，就是基于 Attachment(TypedDict) 重新定义一份 pydantic 版本，并：
        - 修改原先声明 NotRequired 字段为 Optional
        - 提供一些默认初始值
    """
    id: Snowflake
    filename: str
    size: int
    url: str
    proxy_url: str
    height: int = None
    width: int = None
    description: str = None
    content_type: str = None
    spoiler: bool = False
    ephemeral: bool = False


class ICallback(MyBaseModel):
    type: str
    id: int
    content: str
    attachments: List[IAttachment]
    
    trigger_id: TriggerID
    trigger_status: TriggerStatus
