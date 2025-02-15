from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from ..core.config import settings

scheduler = AsyncIOScheduler(
    jobstores={
        'default': SQLAlchemyJobStore(url=settings.DATABASE_URL)
    }
)

# Remove the automatic scheduler.start()