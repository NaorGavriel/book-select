"""
Shared Redis client factory.

Provides a singleton Redis client reusing the jobs Redis instance,
used by both in-process instrumentation and FastAPI dependencies.
"""
import redis as redis_lib
from app.core.config.config import settings

_redis_client: redis_lib.Redis | None = None


def get_redis_client() -> redis_lib.Redis:
    """Return a singleton Redis client connected to the jobs Redis instance."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis_lib.from_url(settings.REDIS_JOBS_URL, decode_responses=True)
    return _redis_client
