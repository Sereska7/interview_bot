"""Category models."""

from bot.pkg.models.base import BaseModel


__all__ = [
    "Category"
]


class BaseCategory(BaseModel):
    """Base model for Category."""


class Category(BaseCategory):
    """"""

    category_id: int
    name: str
    description: str | None
