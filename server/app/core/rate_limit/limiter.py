from slowapi import Limiter
from app.core.rate_limit.util import rate_limit_key
from app.core.config import GeneralConfig

limiter = Limiter(key_func=rate_limit_key,
                    storage_uri=GeneralConfig.REDIS_RATELIMIT_URL)