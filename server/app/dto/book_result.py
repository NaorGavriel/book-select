from dataclasses import dataclass
from app.models.enums import Decision

@dataclass
class BookResult:
    user_id: int
    title: str
    authors: list[str]
    decision: Decision
    confidence: float
    explanation: str