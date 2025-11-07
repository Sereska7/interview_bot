from sqlalchemy import func
from sqlalchemy.sql.expression import select

from bot.internal.repository.repository import Repository
from bot.internal.repository.v1.postgresql.connection import get_connection
from bot.internal.repository.v1.postgresql.handlers.collect_response import collect_response
from bot.pkg.models.sql_models import Question, Category
from bot.pkg.models import v1 as models


class CategoryRepository(Repository):
    """Category repository implementation."""

    @collect_response
    async def get_categories(self) -> list[models.Category]:
        """"""

        async with get_connection() as session:
            result = await session.execute(select(Category))
            return result.scalars().all()