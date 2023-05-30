import json
import time

import aiohttp
from discord import Message
from discord.ext.commands import Bot
from starlette.websockets import WebSocket

import settings_discord
import settings_server
from src.ds.discord import TriggerStatus, ICallback, IAttachment
from src.lib.fetch import fetch
from src.lib.log import logger
from src.lib.path import DATA_DIR
from src.lib.store import set_temp, pop_temp, get_temp
from src.lib.utils import match_trigger_id


def register_discord_handlers(bot: Bot):
    @bot.event
    async def on_ready():
        logger.success(f"Logged in as {bot.user} (ID: {bot.user.id})")
    
    @bot.event
    async def on_message(message: Message):
        if message.author.id != 936929561302675456:
            return
        
        logger.debug(f"on_message: {message}")
        content = message.content
        trigger_id = match_trigger_id(content)
        if not trigger_id:
            return
        
        if content.find("Waiting to start") != -1:
            type_ = TriggerStatus.start
            set_temp(trigger_id)
        elif content.find("(Stopped)") != -1:
            type_ = TriggerStatus.error
            pop_temp(trigger_id)
        else:
            type_ = TriggerStatus.end
            pop_temp(trigger_id)
        
        await callback(ICallback(
            type=type_,
            id=message.id,
            content=content,
            attachments=[IAttachment.parse_obj(attachment.to_dict()) for attachment in message.attachments],
            trigger_id=trigger_id,
            trigger_status=TriggerStatus.message,
        ))
    
    @bot.event
    async def on_message_edit(_: Message, message: Message):
        if message.author.id != 936929561302675456:
            return
        
        trigger_id = match_trigger_id(message.content)
        if not trigger_id:
            return
        
        logger.debug(f"on_message_edit: {message}")
        if message.attachments:
            print({"attachments": message.attachments})
            print()
        if message.webhook_id != "":
            await callback(ICallback(
                type=TriggerStatus.generating,
                id=message.id,
                content=message.content,
                attachments=[IAttachment.parse_obj(attachment.to_dict()) for attachment in message.attachments],
                trigger_id=trigger_id,
                trigger_status=TriggerStatus.edit,
            ))
    
    @bot.event
    async def on_message_delete(message: Message):
        if message.author.id != 936929561302675456:
            return
        
        trigger_id = match_trigger_id(message.content)
        if not trigger_id:
            return
        
        logger.debug(f"on_message_delete: {message}")
        if get_temp(trigger_id) is None:
            return
        
        logger.warning(f"sensitive content: {message}")
        await callback(ICallback(
            type=TriggerStatus.banned,
            id=message.id,
            content=message.content,
            attachments=[IAttachment.parse_obj(attachment.to_dict()) for attachment in message.attachments],
            trigger_id=trigger_id,
            trigger_status=TriggerStatus.delete
        ))


async def callback(data: ICallback, websocket: WebSocket = None):
    if settings_discord.DUMP_CALLBACK_DATA:
        with open(DATA_DIR / f"callback-{time.time()}.json", "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.debug(f"callback data: {data}")
    
    if settings_server.WEBSOCKET_ENABLED and websocket:
        logger.debug(f"sending to {websocket}")
        await websocket.send_json(data)
        return
    
    if not settings_discord.CALLBACK_URL:
        logger.warning("没有配置 CALLBACK_URL，因此忽略回调数据")
        return
    
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=30),
        headers=headers
    ) as session:
        logger.debug(f"fetching callback_url")
        await fetch(session, settings_discord.CALLBACK_URL, json=data)
