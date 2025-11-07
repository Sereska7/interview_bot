from uuid import UUID

from sqlalchemy.sql.expression import select

from bot.internal.repository.repository import Repository
from bot.internal.repository.v1.postgresql.connection import get_connection
from bot.internal.repository.v1.postgresql.handlers.collect_response import collect_response
from bot.pkg.models.sql_models import UserProfile
from bot.pkg.models.sql_models.subscription import Subscription

from bot.pkg.models import v1 as models

class UserProfileRepository(Repository):
    """"""

    @collect_response
    async def create(
        self,
        cmd: models.UserProfileCreateCommand
    ) -> models.UserProfile:
        """"""
        async with get_connection() as session:
            user_profile = UserProfile(
                user_id=cmd.user_id,
            )
            session.add(user_profile)
            await session.flush()

            return user_profile

    @collect_response
    async def get_by_user_id(
        self,
        user_id: UUID
    ) -> models.UserProfile | None:
        """"""
        async with get_connection() as session:
            result = await session.execute(
                select(UserProfile).where(UserProfile.user_id == user_id)
            )
            return result.scalar_one_or_none()
