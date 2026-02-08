from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from app.tasks import example_task
from app.db import engine, SessionLocal
from app.models.base import Base
from app.models.jobs import Job

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

