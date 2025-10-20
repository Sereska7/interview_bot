from bot.internal.repository.v1.postgresql.user import UserRepository
from bot.pkg.models import v1 as models


class UserService:
    """User services class."""

    user_repository: UserRepository

    async def create_user(
        self,
        cmd: models.CreateUser
    ):
        """"""
        existing_user = await self.user_repository.get_by_telegram_id(cmd.telegram_id)
        if existing_user:
            print("Пользователь существует")
            return existing_user
        return await self.user_repository.create(cmd)

    async def get_by_telegram_id(
        self,
        user_tg_id: int
    ):
        return await self.user_repository.get_by_telegram_id(user_tg_id)
