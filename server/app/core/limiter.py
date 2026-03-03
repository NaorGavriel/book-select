from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import RATELIMIT_REDIS_URL

limiter = Limiter(key_func=get_remote_address,
                    storage_uri=RATELIMIT_REDIS_URL)