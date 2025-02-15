from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class TriggerBase(BaseModel):
    type: str
    schedule: Optional[str] = None
    api_schema: Optional[Dict[str, Any]] = None
    recurring: Optional[bool] = False  # Add this field
    recurring_pattern: Optional[str] = None  # Add this field

class TriggerCreate(TriggerBase):
    pass

class Trigger(TriggerBase):
    id: uuid.UUID
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True