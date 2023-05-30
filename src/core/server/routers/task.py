from fastapi import APIRouter

from src.ds import TriggerID
from src.ds.discord import ICallback
from src.lib.store import trigger_manager

trigger_router = APIRouter(prefix='/trigger', tags=['trigger'])


@trigger_router.get('',
    # response_model=ITriggerManager
)
async def list_triggers():
    return trigger_manager


@trigger_router.post('',
    # response_model=CallbackDict
)
async def set_trigger(data: ICallback):
    trigger_manager[data.trigger_id] = data
    return data


@trigger_router.get('/{trigger_id}',
    # response_model=Optional[CallbackDict]
)
async def get_trigger(trigger_id: TriggerID):
    return trigger_manager.get(trigger_id)
