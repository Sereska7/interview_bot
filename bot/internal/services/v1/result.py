from bot.internal.repository.v1.postgresql import ResultRepository, UserRepository
from bot.pkg.models import v1 as models


class ResultService:

    user_repository: UserRepository
    result_repository: ResultRepository

    async def create_result(
        self,
        cmd: models.ResultCreateCommand,
    ):

        await self.result_repository.create_result(cmd)

    async def get_results_by_session(
        self,
        session_id: int
    ) -> list[models.Result]:

        return await self.result_repository.get_results_by_session(session_id)
