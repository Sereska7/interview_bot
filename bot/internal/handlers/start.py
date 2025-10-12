from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from dependency_injector.wiring import Provide, inject

from bot.internal.keyboards.main import main_menu_kb
from bot.internal.services.v1 import Services as V1Services
from bot.internal.services.v1.user import UserService
from bot.pkg.models import v1 as models
from bot.utils.constants import WELCOME_TEXT, TEXT_MAIN_MENU

router = Router()


@router.message(CommandStart())
@inject
async def start_command(
    message: types.Message,
    state: FSMContext,
    user_service: UserService = Provide[V1Services.user_service]
):
    await state.clear()
    cmd = models.CreateUser(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )

    await user_service.create_user(cmd)

    start_msg = await message.answer(
        WELCOME_TEXT,
        reply_markup=main_menu_kb,
        parse_mode="Markdown"
    )

    await state.update_data(start_msg_id=start_msg.message_id)
    await message.delete()

@router.callback_query(F.data == "back")
async def handle_back(query: types.CallbackQuery, state: FSMContext):
    await query.answer(text="Возврат в главное меню", show_alert=False)
    await state.clear()

    try:
        await query.message.delete()
    except Exception:
        pass

    start_msg: types.Message = await query.message.bot.send_message(
        chat_id=query.message.chat.id,
        text=TEXT_MAIN_MENU,
        reply_markup=main_menu_kb,
        parse_mode="Markdown"
    )

    await state.update_data(start_msg_id=start_msg.message_id)
    await query.answer()
