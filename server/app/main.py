from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import engine
from app.models.base import Base
from app.routes.users import router as users_router
from app.routes.preferences import router as preferences_router
from app.routes.jobs import router as jobs_router
from app.routes.job_results import router as job_results_router
from app.routes.user_book import router as user_book_router
from app.routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import app.models
from app.core.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.logger.logging_middleware import logging_middleware
from app.core.logger.logger import init_logging
from app.core.config import GeneralConfig

# lifespan method, in charge of init required before application startup and shutdowns before application shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    init_logging()  # starting logging thread
    yield

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# attaching cors middleware, allowing requests from listed origins in CORS_ORIGINS enviornment variable
app.add_middleware(
    CORSMiddleware,
    allow_origins=GeneralConfig.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

# attaching logging middleware.
app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)


# including all routers
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(preferences_router, prefix="/api")
app.include_router(jobs_router, prefix="/api")
app.include_router(job_results_router, prefix="/api")
app.include_router(user_book_router, prefix="/api")
