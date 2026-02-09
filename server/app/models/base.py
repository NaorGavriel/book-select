from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import DateTime, func


class Base(DeclarativeBase):
    """
    Declarative base for all ORM models.
    """

    created_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    """Row creation timestamp, set automatically by the database."""

    def as_dict(self) -> dict:
        """
        Return a dictionary of column names to values.
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


