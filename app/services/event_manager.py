from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.event import Event
from ..schemas.event import EventCreate
from ..core.database import SessionLocal, get_db

async def create_event_from_trigger(trigger_id: str):
    """Create event from trigger_id - used by scheduler"""
    db = next(get_db())
    try:
        event = EventCreate(
            trigger_id=trigger_id,
            status="active",
            triggered_at=datetime.utcnow()
        )
        db_event = Event(**event.dict())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_event(db: Session, event: EventCreate):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

async def archive_old_events():
    db = next(get_db())
    try:
        two_hours_ago = datetime.utcnow() - timedelta(hours=2)
        db.query(Event).filter(
            Event.triggered_at <= two_hours_ago,
            Event.status == "active"
        ).update({"status": "archived"})
        db.commit()
    finally:
        db.close()

async def delete_old_events():
    db = next(get_db())
    try:
        forty_eight_hours_ago = datetime.utcnow() - timedelta(hours=48)
        db.query(Event).filter(
            Event.triggered_at <= forty_eight_hours_ago
        ).delete()
        db.commit()
    finally:
        db.close()

async def get_events(db: Session, skip: int = 0, limit: int = 100, status: str = None):
    """Get events with optional status filter"""
    query = db.query(Event)
    if status:
        query = query.filter(Event.status == status)
    return query.offset(skip).limit(limit).all()

async def get_event(db: Session, event_id: str):
    """Get single event by ID"""
    return db.query(Event).filter(Event.id == event_id).first()

async def get_aggregated_events(db: Session, hours: int = 48):
    """Get aggregated events from the last N hours"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    aggregated_events = db.query(
        Event.trigger_id,
        func.count(Event.id).label('count'),
        func.max(Event.triggered_at).label('last_triggered'),
        func.min(Event.triggered_at).label('first_triggered'),
        Event.status
    ).filter(
        Event.triggered_at >= time_threshold
    ).group_by(
        Event.trigger_id,
        Event.status
    ).all()
    
    return aggregated_events

async def get_events_for_trigger(db: Session, trigger_id: str, skip: int = 0, limit: int = 100):
    """Get individual events for a specific trigger"""
    return db.query(Event).filter(
        Event.trigger_id == trigger_id
    ).order_by(
        Event.triggered_at.desc()
    ).offset(skip).limit(limit).all()