from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .api.endpoints import triggers, events, auth
from .core.database import Base, engine
from .services.scheduler import scheduler
from .services.event_manager import archive_old_events, delete_old_events
from apscheduler.jobstores.base import ConflictingIdError
from app.core.config import settings
from sqlalchemy import create_engine
from app.api.routers.health import router as health_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Trigger Platform")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(triggers.router, prefix="/api/v1/triggers", tags=["triggers"])
app.include_router(events.router, prefix="/api/v1/events", tags=["events"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def root():
    return {"message": "Event Trigger Platform API"}

@app.get("/status")
async def status():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

@app.on_event("startup")
async def startup_event():
    if not scheduler.running:
        scheduler.start()
    
    # Add cleanup jobs with conflict handling
    cleanup_jobs = [
        {
            'id': 'archive_old_events',
            'func': archive_old_events,
            'trigger': 'interval',
            'minutes': 30
        },
        {
            'id': 'delete_old_events',
            'func': delete_old_events,
            'trigger': 'interval',
            'hours': 24
        }
    ]

    for job in cleanup_jobs:
        try:
            # Remove existing job if it exists
            scheduler.remove_job(job['id'])
        except:
            pass  # Job doesn't exist yet
        
        try:
            # Add the job
            scheduler.add_job(
                job['func'],
                job['trigger'],
                id=job['id'],
                **{k: v for k, v in job.items() if k not in ['id', 'func', 'trigger']}
            )
        except ConflictingIdError:
            # Job already exists, skip
            pass

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()