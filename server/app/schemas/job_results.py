from pydantic import BaseModel
from pydantic import BaseModel
from typing import List
from app.models.enums import Decision

class JobResultItem(BaseModel):
    """
    Representation of a single job result.

    Mirrors the JobResult ORM model, safe to expose externally via the API.
    """
    title: str
    authors: List[str]
    decision: Decision
    confidence: float
    explanation: str

    class Config:
        from_attributes = True

