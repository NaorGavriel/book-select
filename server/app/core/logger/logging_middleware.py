from fastapi import Request
import logging
import os

API_LOGGER_NAME = os.getenv("API_LOGGER_NAME")
logger = logging.getLogger(API_LOGGER_NAME)

async def logging_middleware(request : Request, call_next):
    log_fields_extra = {
        'url' : request.url.path,
        'method' : request.method
    }
    logger.info("api call", extra=log_fields_extra)

    response = await call_next(request)
    return response