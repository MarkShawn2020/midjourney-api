from fastapi import APIRouter, HTTPException

from src.ds import TriggerID, ITriggerCallback, ITriggerManager

trigger_router = APIRouter(prefix='/trigger', tags=['trigger'])

trigger_manager: ITriggerManager = {}


@trigger_router.get('', response_model=ITriggerManager)
async def list_triggers():
    return trigger_manager


@trigger_router.post('', response_model=ITriggerCallback)
async def set_trigger(data: ITriggerCallback):
    trigger_manager[data.id] = data
    return data


@trigger_router.get('/{trigger_id}', response_model=ITriggerCallback)
async def get_trigger(trigger_id: TriggerID):
    result = trigger_manager.get(trigger_id)
    if not result:
        raise HTTPException(404, f"trigger(id={trigger_id}) not exists")
    return result
