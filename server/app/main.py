from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from app.tasks import example_task
from app.db import engine, SessionLocal
from app.models.base import Base
from app.routes.users import router as users_router
import app.models




@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users_router, prefix="/api")

