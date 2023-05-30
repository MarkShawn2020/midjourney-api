from fastapi import APIRouter

from src.core.server.routers.midjourney import midjourney_router
from src.core.server.routers.task import trigger_router

root_router = APIRouter()

root_router.include_router(trigger_router)
root_router.include_router(midjourney_router)
