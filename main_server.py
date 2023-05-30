import uvicorn
from fastapi import FastAPI
from fastapi_socketio import SocketManager

import settings_server  # noqa
from src.core.server.handlers import exc_handler
from src.core.server.routers import root_router


def init_app():
    _app = FastAPI(title="Midjourney API")
    
    _app.include_router(root_router, prefix=settings_server.API_PREFIX)
    exc_handler(_app)
    
    _sm = SocketManager(app=_app)
    
    return _app, _sm


app, sm = init_app()


def main(host, port):
    uvicorn.run("main_server:app", host=host, port=port, reload=settings_server.RELOAD_ENABLED)


if __name__ == '__main__':
    main("localhost", 8062)
