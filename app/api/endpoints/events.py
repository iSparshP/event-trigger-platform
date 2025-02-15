from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Union
from ...core.database import get_db
from ...schemas.event import Event, EventAggregate
from ...services.event_manager import (
    get_events, 
    get_event, 
    get_aggregated_events,
    get_events_for_trigger
)
from ...core.security import get_current_user
from ...schemas.user import User

router = APIRouter()

@router.get("/", response_model=Union[List[Event], List[EventAggregate]])
async def list_events(
    skip: int = 0,
    limit: int = 100,
    status: str = Query(None, enum=['active', 'archived']),
    aggregate: bool = Query(False, description="Aggregate events by trigger"),
    hours: int = Query(48, description="Hours to look back for aggregation"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if aggregate:
        return await get_aggregated_events(db, hours=hours)
    return await get_events(db, skip=skip, limit=limit, status=status)

@router.get("/trigger/{trigger_id}", response_model=List[Event])
async def list_trigger_events(
    trigger_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get individual events for a specific trigger"""
    events = await get_events_for_trigger(db, trigger_id, skip=skip, limit=limit)
    if not events:
        raise HTTPException(status_code=404, detail="No events found for this trigger")
    return events

@router.get("/{event_id}", response_model=Event)
async def get_event_by_id(event_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = await get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
