import redis.asyncio as aioredis
from app.core.config import settings
import logging
import json
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Redis Client (singleton) 
redis_client: Optional[aioredis.Redis] = None


async def get_redis() -> aioredis.Redis:
    """
    Returns the Redis client.
    FastAPI dependency — use with Depends(get_redis)
    """
    global redis_client
    if redis_client is None:
        redis_client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return redis_client


async def close_redis():
    """Close Redis connection on app shutdown"""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


#Cache Helpers 
class CacheService:
    """
    Simple Redis cache wrapper.
    Used for: ICD-10 lookups, eligibility results, payer rules.
    """

    def __init__(self, redis: aioredis.Redis):
        self.redis = redis
        self.ttl = settings.REDIS_TTL_SECONDS

    async def get(self, key: str) -> Optional[Any]:
        """Get cached value — returns None if not found"""
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Cache a value with optional TTL override"""
        await self.redis.setex(
            key,
            ttl or self.ttl,
            json.dumps(value)
        )

    async def delete(self, key: str) -> None:
        """Remove a cached value"""
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        return bool(await self.redis.exists(key))

    async def flush_pattern(self, pattern: str) -> int:
        """Delete all keys matching a pattern e.g. 'icd10:*'"""
        keys = await self.redis.keys(pattern)
        if keys:
            return await self.redis.delete(*keys)
        return 0

    #Tenant-scoped cache keys 
    @staticmethod
    def tenant_key(tenant_id: str, key: str) -> str:
        """Prefix cache key with tenant ID for isolation"""
        return f"tenant:{tenant_id}:{key}"

    @staticmethod
    def icd10_key(code: str) -> str:
        return f"mcr:icd10:{code}"

    @staticmethod
    def cpt_key(code: str) -> str:
        return f"mcr:cpt:{code}"

    @staticmethod
    def eligibility_key(patient_id: str, payer_id: str) -> str:
        return f"eligibility:{patient_id}:{payer_id}"

    @staticmethod
    def payer_rules_key(payer_id: str, cpt: str) -> str:
        return f"prb:{payer_id}:{cpt}"


#Health Check 
async def check_redis_connection() -> bool:
    """Verify Redis is reachable — used in /health endpoint"""
    try:
        client = await get_redis()
        await client.ping()
        return True
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        return False
