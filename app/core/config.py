from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str # Remove default value to force env var usage
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENVIRONMENT: str = "development"
    REDIS_URL: str = "redis://localhost:6379/0"
    EVENT_CACHE_TTL: int = 300  # 5 minutes
    EVENT_ARCHIVE_HOURS: int = 2
    EVENT_DELETE_HOURS: int = 48
    
    class Config:
        env_file = ".env"

settings = Settings()

