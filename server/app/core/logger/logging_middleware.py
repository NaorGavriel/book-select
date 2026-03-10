from fastapi import Request
import logging
import os
from app.core.config.config import settings

logger = logging.getLogger(settings.API_LOGGER_NAME)

async def logging_middleware(request : Request, call_next):
    log_fields_extra = {
        'url' : request.url.path,
        'method' : request.method
    }
    logger.info("API", extra=log_fields_extra)

    response = await call_next(request)
    return response