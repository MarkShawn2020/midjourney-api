import asyncio
from functools import wraps

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from src.core.discord.main import init_discord_bot
from starlette import status
from starlette.responses import JSONResponse

import settings
from src.ds import TriggerStatus, ITrigger
from src.lib.exceptions import APPBaseException
from src.lib.log import logger


def exc_handler(app: FastAPI):
    @app.on_event("startup")
    async def startup():
        logger.info(f"DISCORD_EMBED_IN_FASTAPI_ENABLED: {settings.DISCORD_EMBED_IN_FASTAPI_ENABLED}")
        if settings.DISCORD_EMBED_IN_FASTAPI_ENABLED:
            bot = init_discord_bot()
            asyncio.create_task(bot.start(settings.DISCORD_BOT_TOKEN))
    
    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(_, exc: RequestValidationError):
        logger.debug(exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"request params error: {exc.body}",
        )
    
    @app.exception_handler(APPBaseException)
    def validation_exception_handler(_, exc: APPBaseException):
        logger.debug(exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=exc.message,
        )


def http_response(func):
    @wraps(func)
    async def router(*args, **kwargs):
        trigger_id, resp = await func(*args, **kwargs)
        if resp is not None:
            code, trigger_status = status.HTTP_200_OK, TriggerStatus.success
        else:
            code, trigger_status = status.HTTP_400_BAD_REQUEST, TriggerStatus.fail
        
        return JSONResponse(
            status_code=code,
            content=ITrigger(id=trigger_id, status=trigger_status).dict()
        )
    
    return router
