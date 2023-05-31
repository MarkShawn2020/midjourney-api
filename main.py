import uvicorn
from fastapi import FastAPI
from fastapi_socketio import SocketManager

import settings
from src.core.server.handlers import exc_handler
from src.core.server.routers import root_router


def init_app():
    _app = FastAPI(title="Midjourney API")
    
    _app.include_router(root_router, prefix=settings.API_PREFIX)
    exc_handler(_app)
    
    _sm = None
    if settings.DISCORD_WEBSOCKET_ENABLED:
        _sm = SocketManager(app=_app)
    
    return _app, _sm


app, sm = init_app()

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8062, reload=settings.UVICORN_RELOAD_ENABLED)
