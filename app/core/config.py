from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application Settings
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "triggers"
    DB_PORT: int = 5432
    DATABASE_URL: str
    
    # Redis Settings
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Event Settings
    EVENT_CACHE_TTL: int = 300
    EVENT_ARCHIVE_HOURS: int = 2
    EVENT_DELETE_HOURS: int = 48

    model_config = {
        "env_file": ".env",
        "extra": "allow"  # This allows extra fields from env vars
    }

settings = Settings()

