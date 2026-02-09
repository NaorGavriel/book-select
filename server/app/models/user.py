from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer

from app.models.base import Base


class User(Base):
    """
    Represents an registered user of the system.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    email: Mapped[str] = mapped_column(String, unique=True, index=True)

    password_hash: Mapped[str] = mapped_column(String)

    # One-to-one relationship to the user's preferences
    preferences = relationship(
        "UserPreferences",
        back_populates="user",
        uselist=False
    )

    # One-to-many relationship to jobs submitted by the user
    jobs = relationship("Job", back_populates="user")
