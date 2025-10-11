from sqlalchemy.sql.expression import select

from bot.internal.repository.repository import Repository
from bot.internal.repository.v1.postgresql.connection import get_connection
from bot.pkg.models.sql_models.user import User
from bot.pkg.models import v1 as models


class UserRepository(Repository):
    """User repository implementation."""

    async def get_by_telegram_id(self, telegram_id: int):
        async with get_connection() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            return result.scalar_one_or_none()

    async def create(
        self,
        cmd: models.CreateUser
    ):
        async with get_connection() as session:
            user = User(
                telegram_id=cmd.telegram_id,
                username=cmd.username,
                first_name=cmd.first_name
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

            return user
