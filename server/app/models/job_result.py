from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, Float, String
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base
from app.models.enums import Decision


class JobResult(Base):
    """
    Represents the outcome of evaluating a single book for a given job.

    Each row captures the final recommendation decision, its confidence
    score, and an explanation for the decision.
    """

    __tablename__ = "job_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        index=True
    )

    # Job that produced this result
    job_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("jobs.id"),
        index=True
    )

    # Book being evaluated
    title: Mapped[str] = mapped_column(String)
    authors : Mapped[list[str]] = mapped_column(JSONB, default=dict)

    # Discrete recommendation category (strong_match / consider / avoid)
    decision: Mapped[Decision] = mapped_column(index=True)

    # Normalized score (0.0–1.0) representing recommendation strength
    confidence: Mapped[float] = mapped_column(Float)

    # justification for the decision
    explanation: Mapped[str] = mapped_column(String)

    job = relationship("Job", back_populates="results")
