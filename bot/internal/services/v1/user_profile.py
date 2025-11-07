from bot.internal.repository.v1.postgresql.user_profile import UserProfileRepository
from bot.pkg.models import v1 as models


class UserProfileService:
    user_profile_repository: UserProfileRepository


    async def create_profile(
        self,
        cmd: models.UserProfileCreateCommand
    ) -> models.UserProfile:
        """"""
        existing_user = await self.user_profile_repository.get_by_user_id(cmd.user_id)
        if existing_user:
            return existing_user
        return await self.user_profile_repository.create(cmd)
