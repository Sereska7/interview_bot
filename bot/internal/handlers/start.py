from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from dependency_injector.wiring import Provide, inject

from bot.pkg.keyboards.main import main_menu_kb
from bot.internal.services.v1 import Services as V1Services
from bot.internal.services.v1.user import UserService
from bot.pkg.models import v1 as models
from bot.utils.constants import WELCOME_TEXT, TEXT_MAIN_MENU, escape_md
from bot.utils import delete_old_messages, save_message_id


router = Router()


@router.message(CommandStart())
@inject
async def start_command(
    message: types.Message,
    state: FSMContext,
    user_service: UserService = Provide[V1Services.user_service]
):
    """
    Обрабатывает команду /start и инициализирует пользователя.

    Args:
        message (types.Message): Объект входящего сообщения от Telegram.
        state (FSMContext): Контекст состояний FSM для текущего пользователя.
        user_service (UserService): Сервис для создания или обновления пользователя.

    Returns:
        None: Отправляет приветственное сообщение с главным меню и обновляет состояние пользователя.
    """

    await delete_old_messages(message.bot, message.chat.id, state)
    await message.delete()

    cmd = models.CreateUser(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )

    user = await user_service.create_user(cmd)
    await state.update_data(user_id=user.user_id)

    start_msg = await message.answer(
        WELCOME_TEXT,
        reply_markup=main_menu_kb,
        parse_mode="Markdown"
    )

    await state.update_data({
        "topic": None,
        "level": None,
        "questions": None,
        "current_q": 0,
        "answers": []
    })

    await save_message_id(state, start_msg.message_id)
    await state.update_data(start_msg_id=start_msg.message_id)


@router.callback_query(F.data == "back_main")
async def handle_back(query: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает нажатие кнопки 'На главную'.

    Args:
        query (types.CallbackQuery): Объект callback query от Telegram.
        state (FSMContext): Контекст состояний FSM для текущего пользователя.

    Returns:
        None: Сбрасывает состояние текущего теста, удаляет старое сообщение
        и отправляет главное меню пользователю.
    """

    await query.answer(text="Возврат в главное меню", show_alert=False)
    await state.update_data({
        "topic": None,
        "level": None,
        "questions": None,
        "current_q": 0,
        "answers": []
    })

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
    await save_message_id(state, start_msg.message_id)
