import random

from aiogram.fsm.context import FSMContext

from bot.internal.repository.v1.postgresql.category import CategoryRepository
from bot.internal.repository.v1.postgresql.question import QuestionRepository
from bot.pkg.models import v1 as models
from bot.pkg.models.sql_models.question import DifficultyLevel
from bot.utils import save_message_id


class CategoryService:
    """Question services class."""

    category_repository: CategoryRepository

    async def get_categories(self) -> list[models.Category]:
        """"""
        return await self.category_repository.get_categories()