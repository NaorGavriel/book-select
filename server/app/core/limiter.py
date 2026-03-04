from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import GeneralConfig

limiter = Limiter(key_func=get_remote_address,
                    storage_uri=GeneralConfig.REDIS_RATELIMIT_URL)