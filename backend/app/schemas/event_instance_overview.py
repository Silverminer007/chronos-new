from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventInstanceSchema(BaseModel):
    uid: str
    id: Optional[int]
    calendar: Optional[int]
    calendar_name: Optional[str]
    dtstart: Optional[datetime]
    dtend: Optional[datetime]
    summary: Optional[str]
    status: Optional[str]
    class_: Optional[str]
    transp: Optional[str]
    accepted: Optional[int]
    declined: Optional[int]
    needs_action: Optional[int]

    class Config:
        orm_mode = True
