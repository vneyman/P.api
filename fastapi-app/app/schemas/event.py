from datetime import datetime
from pydantic import BaseModel


class EventUpsert(BaseModel):
    name: str
    description: str


class EventOut(BaseModel):
    id: int
    name: str
    description: str
    date_insert: datetime
    date_update: datetime
