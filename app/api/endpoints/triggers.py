from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from typing import List
from croniter import croniter
from ...core.database import get_db
from ...schemas.trigger import TriggerCreate, Trigger
from ...schemas.event import EventCreate
from ...models.trigger import Trigger as TriggerModel
from ...services.scheduler import scheduler
from ...services.event_manager import create_event, create_event_from_trigger
from ...core.security import get_current_user
from ...schemas.user import User

router = APIRouter()

@router.post("/", response_model=Trigger)
async def create_trigger(
    trigger: TriggerCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate trigger type
    if trigger.type not in ['scheduled', 'api']:
        raise HTTPException(status_code=400, detail="Invalid trigger type. Must be 'scheduled' or 'api'")
    
    # Additional validation for string fields
    if trigger.type == "string":
        raise HTTPException(status_code=400, detail="'string' is not a valid trigger type")
        
    # Validate schedule format
    if trigger.type == "scheduled":
        if trigger.recurring and not croniter.is_valid(trigger.recurring_pattern):
            raise HTTPException(status_code=400, detail="Invalid cron expression")
    
    # Validate API schema
    if trigger.type == "api":
        if not trigger.api_schema or not isinstance(trigger.api_schema, dict):
            raise HTTPException(status_code=400, detail="Invalid API schema")
        if "required_fields" not in trigger.api_schema:
            raise HTTPException(status_code=400, detail="API schema must specify required_fields")

    db_trigger = TriggerModel(**trigger.dict())
    db.add(db_trigger)
    db.commit()
    db.refresh(db_trigger)
    
    if trigger.type == "scheduled" and trigger.recurring:
        try:
            # Parse the cron expression manually
            minute, hour, day, month, day_of_week = trigger.recurring_pattern.split()
            scheduler.add_job(
                create_event_from_trigger,  # Direct function reference
                'cron',
                args=[str(db_trigger.id)],  # Pass trigger_id as string
                minute=minute,
                hour=hour,
                day=day,
                month=month,
                day_of_week=day_of_week,
                id=str(db_trigger.id)
            )
        except Exception as e:
            # Clean up if scheduler fails
            db.delete(db_trigger)
            db.commit()
            raise HTTPException(status_code=500, detail=f"Failed to schedule trigger: {str(e)}")
    elif trigger.type == "scheduled" and trigger.schedule:
        try:
            scheduler.add_job(
                create_event_from_trigger,  # Direct function reference
                'date',
                run_date=trigger.schedule,
                args=[str(db_trigger.id)],  # Pass trigger_id as string
                id=str(db_trigger.id)
            )
        except Exception as e:
            # Clean up if scheduler fails
            db.delete(db_trigger)
            db.commit()
            raise HTTPException(status_code=500, detail=f"Failed to schedule trigger: {str(e)}")
    
    return db_trigger


@router.get("/", response_model=List[Trigger])
async def list_triggers(
    type: str = Query(None, enum=['scheduled', 'api']),
    is_active: bool = Query(None),
    recurring: bool = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(TriggerModel)
    
    if type:
        query = query.filter(TriggerModel.type == type)
    if is_active is not None:
        query = query.filter(TriggerModel.is_active == is_active)
    if recurring is not None:
        query = query.filter(TriggerModel.recurring == recurring)
        
    triggers = query.order_by(TriggerModel.created_at.desc()).all()
    return triggers

@router.put("/{trigger_id}", response_model=Trigger)
async def update_trigger(
    trigger_id: str, 
    trigger: TriggerCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        db_trigger = db.query(TriggerModel).filter(TriggerModel.id == trigger_id).first()
        if not db_trigger:
            raise HTTPException(status_code=404, detail="Trigger not found")
        
        # Validate schedule format for scheduled triggers
        if trigger.type == "scheduled":
            if trigger.recurring and not croniter.is_valid(trigger.recurring_pattern):
                raise HTTPException(status_code=400, detail="Invalid cron expression")
            if not trigger.recurring and not trigger.schedule:
                raise HTTPException(status_code=400, detail="Either schedule or recurring_pattern must be provided")
        
        # Validate API schema for API triggers
        if trigger.type == "api":
            if not trigger.api_schema or not isinstance(trigger.api_schema, dict):
                raise HTTPException(status_code=400, detail="Invalid API schema")
            if "required_fields" not in trigger.api_schema:
                raise HTTPException(status_code=400, detail="API schema must specify required_fields")
        
        # Remove old scheduled job if exists
        if db_trigger.type == "scheduled":
            try:
                scheduler.remove_job(str(db_trigger.id))
            except Exception as e:
                # Log the error but continue if job doesn't exist
                print(f"Error removing old job: {e}")
        
        # Begin transaction
        db.begin()
        
        # Update trigger fields
        update_data = trigger.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_trigger, key, value)
        
        # Add new schedule if needed
        if trigger.type == "scheduled":
            try:
                if trigger.recurring:
                    minute, hour, day, month, day_of_week = trigger.recurring_pattern.split()
                    scheduler.add_job(
                        create_event_from_trigger,
                        'cron',
                        args=[str(db_trigger.id)],
                        minute=minute,
                        hour=hour,
                        day=day,
                        month=month,
                        day_of_week=day_of_week,
                        id=str(db_trigger.id)
                    )
                elif trigger.schedule:
                    scheduler.add_job(
                        create_event_from_trigger,
                        'date',
                        run_date=trigger.schedule,
                        args=[str(db_trigger.id)],
                        id=str(db_trigger.id)
                    )
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=500, detail=f"Failed to update trigger schedule: {str(e)}")
        
        db.commit()
        db.refresh(db_trigger)
        return db_trigger
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update trigger: {str(e)}")

@router.delete("/{trigger_id}")
async def delete_trigger(
    trigger_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trigger = db.query(TriggerModel).filter(TriggerModel.id == trigger_id).first()
    if not trigger:
        raise HTTPException(status_code=404, detail="Trigger not found")
    
    if trigger.type == "scheduled":
        scheduler.remove_job(str(trigger.id))
    
    db.delete(trigger)
    db.commit()
    return {"message": "Trigger deleted"}

@router.post("/{trigger_id}/test")
async def test_trigger(
    trigger_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trigger = db.query(TriggerModel).filter(TriggerModel.id == trigger_id).first()
    if not trigger:
        raise HTTPException(status_code=404, detail="Trigger not found")
    
    # Create test event
    event = await create_event(db, EventCreate(
        trigger_id=trigger.id,
        is_test=True
    ))
    return {"message": "Test trigger executed", "event_id": event.id}

@router.post("/{trigger_id}/trigger")
async def trigger_api_endpoint(
    trigger_id: str, 
    request: Request, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trigger = db.query(TriggerModel).filter(TriggerModel.id == trigger_id).first()
    if not trigger:
        raise HTTPException(status_code=404, detail="Trigger not found")
    
    if trigger.type != "api":
        raise HTTPException(status_code=400, detail="Not an API trigger")
    
    # Validate request body against schema
    body = await request.json()
    required_fields = trigger.api_schema.get("required_fields", [])
    for field in required_fields:
        if field not in body:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    # Create event
    event = await create_event(db, EventCreate(
        trigger_id=trigger.id,
        payload=body
    ))
    return {"message": "API trigger executed", "event_id": event.id}