from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class EventBase(BaseModel):
    trigger_id: uuid.UUID
    payload: Optional[Dict[str, Any]] = None
    is_test: bool = False

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: uuid.UUID
    triggered_at: datetime
    status: str

    class Config:
        from_attributes = True

class EventAggregate(BaseModel):
    trigger_id: uuid.UUID
    count: int
    last_triggered: datetime
    first_triggered: datetime
    status: str
    
    class Config:
        from_attributes = True
