from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from dependency_injector.wiring import Provide, inject

from bot.internal.keyboards.main import main_menu_kb
from bot.internal.services.v1 import Services as V1Services
from bot.internal.services.v1.user import UserService
from bot.pkg.models import v1 as models
from bot.utils.constants import WELCOME_TEXT

router = Router()


@router.message(CommandStart())
@inject
async def start_command(
    message: types.Message,
    state: FSMContext,
    user_service: UserService=Provide[V1Services.user_service]
):
    cmd = models.CreateUser(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )

    await user_service.create_user(cmd)

    await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb, parse_mode="Markdown")
