from sqlalchemy import Column, String, DateTime, JSON, UUID, Boolean, CheckConstraint
from sqlalchemy.sql import func
import uuid
from ..core.database import Base

class Trigger(Base):
    __tablename__ = "triggers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String, nullable=False)  # "scheduled" or "api"
    schedule = Column(String, nullable=True)
    api_schema = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    recurring = Column(Boolean, default=False)
    recurring_pattern = Column(String, nullable=True)  # cron expression for recurring schedules
    api_endpoint = Column(String, nullable=True)  # endpoint path for API triggers
    api_method = Column(String, nullable=True)  # HTTP method for API triggers

    # Add constraint to validate trigger type
    __table_args__ = (
        CheckConstraint(
            type.in_(['scheduled', 'api']),
            name='check_trigger_type'
        ),
    )

