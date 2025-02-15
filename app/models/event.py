from sqlalchemy import Column, String, DateTime, JSON, UUID, Boolean, ForeignKey
from sqlalchemy.sql import func
import uuid
from ..core.database import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trigger_id = Column(UUID(as_uuid=True), ForeignKey("triggers.id"))
    payload = Column(JSON, nullable=True)
    triggered_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="active")  # active, archived, deleted
    is_test = Column(Boolean, default=False)