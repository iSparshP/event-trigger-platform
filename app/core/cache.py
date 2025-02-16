from redis import Redis
from ..core.config import settings
import json

redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)

async def cache_get(key: str):
    data = redis_client.get(key)
    return json.loads(data) if data else None

async def cache_set(key: str, value: dict, expire: int = 3600):
    redis_client.setex(key, expire, json.dumps(value))

async def cache_delete(key: str):
    redis_client.delete(key)
