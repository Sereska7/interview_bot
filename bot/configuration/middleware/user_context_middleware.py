from aiogram import BaseMiddleware

from bot.internal.services.v1 import UserService
from bot.internal.services.v1.user_profile import UserProfileService
from bot.pkg.models import v1 as models


class UserContextMiddleware(BaseMiddleware):
    user_service: UserService
    user_profile_service: UserProfileService

    async def __call__(self, handler, event, data):
        state = data.get("state")
        user = data.get("event_from_user")

        if state and user:
            data_state = await state.get_data()
            if not data_state.get("user_id"):
                cmd = models.UserCreateCommand(
                    telegram_id=user.id,
                    username=user.username,
                    first_name=user.first_name,
                )
                user_obj = await self.user_service.create_user(cmd)
                cmd = models.UserProfileCreateCommand(
                    user_id=user_obj.user_id
                )
                user_profile = await self.user_profile_service.create_profile(cmd)

                await state.update_data(
                    user_id=user_obj.user_id,
                    current_grade=user_profile.current_grade
                )

        return await handler(event, data)
