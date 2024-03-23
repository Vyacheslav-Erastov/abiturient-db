from enum import Enum
from uuid import UUID
from pydantic import BaseModel


class EventWS(str, Enum):
    TASK_CREATE = "TASK_CREATE"
    TASK_UPDATE = "TASK_UPDATE"
    TASK_DELETE = "TASK_DELETE"
    EVENT_CREATE = "EVENT_CREATE"


class MessageWS(BaseModel):
    event: EventWS
    data: BaseModel | UUID
