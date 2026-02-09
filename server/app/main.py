from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from app.tasks import example_task
from app.db import engine, SessionLocal
from app.models.base import Base
from app.routes.users import router as users_router
from app.routes.preferences import router as preferences_router

import app.models




@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users_router, prefix="/api")
app.include_router(preferences_router, prefix="/api")

