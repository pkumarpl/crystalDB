"""Database base configuration and declarative base."""

from datetime import datetime
from typing import Any

from sqlalchemy import MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Naming convention for constraints (helps with migrations)
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    """Base class for all database models."""

    metadata = metadata

    # Type annotation for improved IDE support
    __tablename__: str


class TimestampMixin:
    """Mixin for created/updated timestamp fields."""

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
        comment="Record creation timestamp",
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Record last update timestamp",
    )
