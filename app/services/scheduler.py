from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from ..core.config import settings

scheduler = AsyncIOScheduler(
    jobstores={
        'default': SQLAlchemyJobStore(url=settings.DATABASE_URL)
    }
)

def init_scheduler():
    # Event cleanup jobs
    scheduler.add_job(
        'app.services.event_manager:archive_old_events',
        'interval',
        minutes=30,
        id='archive_old_events'
    )
    
    scheduler.add_job(
        'app.services.event_manager:delete_old_events',
        'interval',
        hours=24,
        id='delete_old_events'
    )
    
    scheduler.start()