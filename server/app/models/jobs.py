from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, func

from app.models.base import Base
from app.models.enums import JobStatus


class Job(Base):
    """
    Represents an asynchronous image-processing request.

    A Job tracks the lifecycle of a single user request from submission
    (pending) through processing and final completion or failure.
    """

    __tablename__ = "jobs"

    # Unique identifier returned to the client and used for polling
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        index=True
    )

    # storage path to the uploaded image
    image_path: Mapped[str] = mapped_column(String)

    # current state of the asynchronous job
    status: Mapped[JobStatus] = mapped_column(
        default=JobStatus.pending,
        index=True
    )

    # error details if the job fails during processing
    error_message: Mapped[str | None] = mapped_column(String, nullable=True)

    completed_at: Mapped[str | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True
    )

    user = relationship("User", back_populates="jobs")

    # results produced by this job (one per detected book)
    results = relationship("JobResult", back_populates="job")
