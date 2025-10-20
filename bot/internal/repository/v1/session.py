from sqlalchemy import update, func

from bot.internal.repository.repository import Repository
from bot.internal.repository.v1.postgresql.connection import get_connection
from bot.internal.repository.v1.postgresql.handlers.collect_response import collect_response
from bot.pkg.models import v1 as models
from bot.pkg.models.sql_models import Session


class SessionRepository(Repository):

    @collect_response
    async def create(
        self,
        cmd: models.SessionCreateCommand
    ) -> models.Session:

        async with get_connection() as session:
            new_session = Session(
                user_id=cmd.user_id,
                category=cmd.category,
            )

            session.add(new_session)
            await session.commit()
            await session.refresh(new_session)

            return new_session

    @collect_response
    async def update(
        self,
        cmd: models.SessionUpdateCommand
    ) -> models.Session:
        async with get_connection() as session:
            stmt = (
                update(Session)
                .where(Session.session_id == cmd.session_id)
                .values(
                    finished_at=func.now(),
                    score=cmd.score
                )
                .returning(Session)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()

