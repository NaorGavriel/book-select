from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

from app.db import engine, SessionLocal
from app.models import Base, Job

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/jobs")
def create_job():
    db: Session = SessionLocal()
    job = Job(status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)
    db.close()
    return {"id": job.id, "status": job.status}
