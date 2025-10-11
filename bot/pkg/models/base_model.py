"""Base model for SQlAlchemy."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all sql models."""
