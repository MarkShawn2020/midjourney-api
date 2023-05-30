from __future__ import annotations

from enum import StrEnum
from typing import TypeVar, Generic, MutableMapping
from uuid import UUID

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

TriggerID = int


class MyBaseModel(BaseModel):
    class Config:
        use_enum_values = True
        json_encoders = {  # encode, ref: https://docs.pydantic.dev/latest/usage/exporting_models/#json_encoders
            UUID: str,
        }


class TriggerStatus(StrEnum):
    # when trigger
    success = "success"
    fail = "fail"


class ITrigger(MyBaseModel):
    id: TriggerID
    status: TriggerStatus


class ITriggerCallback(ITrigger, GenericModel, Generic[T]):
    result: T = None


ITriggerManager = MutableMapping[TriggerID, ITriggerCallback]
