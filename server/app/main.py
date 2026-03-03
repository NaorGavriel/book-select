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
from app.core.config import CORS_ORIGINS
import app.models

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(preferences_router, prefix="/api")
app.include_router(jobs_router, prefix="/api")
app.include_router(job_results_router, prefix="/api")
app.include_router(user_book_router, prefix="/api")
