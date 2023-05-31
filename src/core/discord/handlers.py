import json
import re
import time
from typing import MutableMapping
from uuid import UUID

import aiohttp
from discord import Message
from discord.ext.commands import Bot
from starlette.websockets import WebSocket

import settings
from settings import DATA_DIR
from src.ds import TriggerStatus, ITriggerCallback, TriggerID
from src.ds.discord import IAttachment, IMessageRaw, IMJMessageCallback, IMessage
from src.ds.midjourney import DrawStatus, IDraw
from src.lib.fetch import fetch
from src.lib.log import logger
from src.lib.utils import get_trigger_id

trigger_uuid_cache: MutableMapping[TriggerID, UUID] = {}


def get_msg_hash(message: Message) -> UUID | None:
    """
    得到 mj 返回的 msg 中的 第一个 attachment 里的 hash 信息，可用于后续获取 mj 官方的 cdn链接
    - 它只在画图完成的时候会出现
    - 并且后续会调用一次 on_message_delete（然后就没有那个hash信息了），因此要做一下缓存
    - 不能用 message.id，因为会一直变，要用 trigger_id
    """
    logger.debug({"uuid_cache": trigger_uuid_cache})
    trigger_id = get_trigger_id(message.content)
    if trigger_id in trigger_uuid_cache:
        return trigger_uuid_cache[trigger_id]
    
    if message.attachments:
        m = re.search(r"_(\S{36})\.", message.attachments[0].filename)  # 36 = 32（uuid位数） + 4(个中折线)
        if m:
            uuid = UUID(m.group(1))
            trigger_uuid_cache[trigger_id] = uuid
            logger.debug({"uuid_cache(updated)": trigger_uuid_cache})
            return uuid
    return None


def get_cdn_url(uuid: UUID, index: int = None) -> str:
    """
    index:
        - None: 四分图
        - 0~3: 每个大图
    """
    if index is not None:
        assert index in range(4)
        slug = f"0_{index}"
    else:
        slug = "grid_0"
    return f"https://cdn.midjourney.com/{uuid}/{slug}_640_N.webp"


def serialize_message(message: Message, draw_status: DrawStatus) -> IMessage:
    logger.debug(f"serializing message: {message}")
    return IMessage(
        raw=IMessageRaw(
            id=message.id,
            content=message.content,
            attachments=[IAttachment.parse_obj(attachment.to_dict()) for attachment in message.attachments],
        ),
        extra=IDraw(
            status=draw_status,
            uuid=get_msg_hash(message),
        )
    )


def get_draw_status(message: Message) -> DrawStatus:
    content = message.content
    if content.find("Waiting to start") != -1:
        return DrawStatus.start
    elif content.find("(Stopped)") != -1:
        return DrawStatus.error
    else:  # todo: more robust validation on potential edge cases
        return DrawStatus.end


def register_discord_handlers(bot: Bot):
    @bot.event
    async def on_ready():
        logger.success(f"Logged in as {bot.user} (ID: {bot.user.id})")
    
    @bot.event
    async def on_message(message: Message):
        if message.author.id != settings.MIDJOURNEY_BOT_ID:  # exclude messages not come from mj bot
            return
        logger.debug(f"on_message: {message}")
        
        await callback(IMJMessageCallback(
            id=get_trigger_id(message.content),
            status=TriggerStatus.success,
            result=serialize_message(message, get_draw_status(message))
        ))
    
    @bot.event
    async def on_message_edit(_: Message, message: Message):
        if message.author.id != settings.MIDJOURNEY_BOT_ID:  # exclude messages not come from mj bot
            return
        logger.debug(f"on_message_edit: {message}")
        
        await callback(IMJMessageCallback(
            id=get_trigger_id(message.content),
            status=TriggerStatus.success,
            result=serialize_message(message, DrawStatus.generating)
        ))
    
    @bot.event
    async def on_message_delete(message: Message):
        if message.author.id != settings.MIDJOURNEY_BOT_ID:  # exclude messages not come from mj bot
            return
        logger.debug(f"on_message_delete: {message}")
        
        await callback(IMJMessageCallback(
            id=get_trigger_id(message.content),
            status=TriggerStatus.success,
            result=serialize_message(message, DrawStatus.deleted)
        ))


async def callback(model: ITriggerCallback, websocket: WebSocket = None):
    data = json.loads(model.json())  # model --> json string --> json dict, (we used UUID), see: https://stackoverflow.com/questions/65622045/pydantic-convert-to-jsonable-dict-not-full-json-string
    if settings.DISCORD_DUMP_CALLBACK_DATA:
        with open(DATA_DIR / f"callback-{time.time()}.json", "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    if settings.DISCORD_WEBSOCKET_ENABLED and websocket:
        logger.debug(f"sending to {websocket}")
        await websocket.send_json(data)
        return
    
    if not settings.DISCORD_CALLBACK_URL:
        logger.warning("没有配置 CALLBACK_URL，因此忽略回调数据")
        return
    
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=30),
        headers=headers
    ) as session:
        logger.debug(f"fetching callback_url")
        await fetch(session, settings.DISCORD_CALLBACK_URL, json=data)
