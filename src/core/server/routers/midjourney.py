from fastapi import APIRouter
from src.core.discord import bridge
from src.core.server.handlers import http_response

from settings import DISCORD_PROMPT_PREFIX, DISCORD_PROMPT_SUFFIX
from src.ds.midjourney import TriggerType, ITriggerImagine, ITriggerUV, ITriggerReset
from src.lib.ban import check_banned
from src.lib.utils import unique_id

midjourney_router = APIRouter(prefix='/midjourney', tags=['midjourney'])


@midjourney_router.post(f"/{TriggerType.imagine}", )
@http_response
async def imagine(body: ITriggerImagine):
    check_banned(body.prompt)
    
    trigger_id = str(unique_id())
    prompt = f"{DISCORD_PROMPT_PREFIX}{trigger_id}{DISCORD_PROMPT_SUFFIX}{body.prompt}"  # 拼接 Prompt 形如: <#1234567890#>a cute cat
    
    return trigger_id, await bridge.imagine(prompt)


@midjourney_router.post(f"/{TriggerType.upscale}", )
@http_response
async def upscale(body: ITriggerUV):
    return body.trigger_id, await bridge.upscale(**body.dict())


@midjourney_router.post(f"/{TriggerType.variation}", )
@http_response
async def variation(body: ITriggerUV):
    return body.trigger_id, await bridge.variation(**body.dict())


@midjourney_router.post(f"/{TriggerType.reset}", )
@http_response
async def reset(body: ITriggerReset):
    return body.trigger_id, await bridge.reset(**body.dict())


@midjourney_router.post(f"/{TriggerType.describe}")
@http_response
async def describe():
    pass


@midjourney_router.post(f"/{TriggerType.upload}")
@http_response
async def upload():
    pass
