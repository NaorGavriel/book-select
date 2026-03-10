import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config.config import settings

engine = create_engine(
    settings.database_url,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


def get_db():
    """
    provides a database session, closes after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
