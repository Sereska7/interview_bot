from bot.internal.repository.v1.session import SessionRepository
from bot.pkg.models import v1 as models

class SessionService:

    session_repository: SessionRepository

    async def create_session(
        self,
        cmd: models.SessionCreateCommand
    ):

        return await self.session_repository.create(cmd)


    async def update_session(
        self,
        cmd: models.SessionUpdateCommand
    ):
        await self.session_repository.update(cmd)
