from sqlalchemy.sql.expression import select

from bot.internal.repository.repository import Repository
from bot.internal.repository.v1.postgresql.connection import get_connection
from bot.internal.repository.v1.postgresql.handlers.collect_response import collect_response
from bot.pkg.models.sql_models.subscription import Subscription
from bot.pkg.models.sql_models.user import User
from bot.pkg.models import v1 as models


class UserRepository(Repository):
    """User repository implementation."""

    @collect_response
    async def get_by_telegram_id(
        self,
        telegram_id: int
    ) -> models.User | None:
        async with get_connection() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            return result.scalar_one_or_none()

    @collect_response
    async def create(
            self,
            cmd: models.CreateUser
    ) -> models.User:
        async with get_connection() as session:
            user = User(
                telegram_id=cmd.telegram_id,
                username=cmd.username,
                first_name=cmd.first_name,
            )
            session.add(user)
            await session.flush()

            subscription = Subscription(
                user_id=user.user_id,
                is_active=True,
                expires_at=None,
            )
            session.add(subscription)

            await session.commit()
            await session.refresh(user)

            return user
