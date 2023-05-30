from __future__ import annotations

from typing import List, Generic

from discord.types.snowflake import Snowflake
from pydantic.generics import GenericModel
from src.ds.midjourney import IDraw

from src.ds import MyBaseModel, ITriggerCallback, T

MessageID = int


class IAttachment(MyBaseModel):
    """
    不要直接用 discord.types.message.Attachment(TypedDict)
        - 会导致 circular import（
            - 官方 discord issues 里搜索也无果：https://github.com/Rapptz/discord.py/issues?q=is%3Aissue+circular
            - 尚不知道 discord 自己是如何没有这个问题的，可能和 partial import 有关，也可能和 TYPE_CHECK 有关
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


class IMessageRaw(MyBaseModel):
    id: MessageID
    content: str
    attachments: List[IAttachment]


class IMessage(MyBaseModel, GenericModel, Generic[T]):
    raw: IMessageRaw
    extra: T


IMJMessageCallback = ITriggerCallback[IMessage[IDraw]]
