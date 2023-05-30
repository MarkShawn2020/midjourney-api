from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T")

TriggerID = int


class MyBaseModel(BaseModel):
    class Config:
        use_enum_values = True
