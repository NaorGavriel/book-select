from slowapi import Limiter
from app.core.rate_limit.util import rate_limit_key
from app.core.config.config import settings

limiter = Limiter(key_func=rate_limit_key,
                    storage_uri=settings.REDIS_RATELIMIT_URL)