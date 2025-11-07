from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from bot.pkg.keyboards.main import main_menu_kb
from bot.utils.constants import WELCOME_TEXT, TEXT_MAIN_MENU
from bot.utils import delete_old_messages, save_message_id


router = Router()


@router.message(CommandStart())
async def start_command(
    message: types.Message,
    state: FSMContext,
):
    await delete_old_messages(message.bot, message.chat.id, state)
    await message.delete()

    msg = await message.answer(
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

    await save_message_id(state, msg.message_id)


@router.message(Command("menu"))
async def show_menu(
    message: types.Message,
    state: FSMContext,
):
    await delete_old_messages(message.bot, message.chat.id, state)

    await state.update_data({
        "topic": None,
        "level": None,
        "questions": None,
        "current_q": 0,
        "answers": []
    })
    start_msg = await message.answer(
        TEXT_MAIN_MENU,
        reply_markup=main_menu_kb,
        parse_mode="Markdown"
    )

    await message.delete()
    await save_message_id(state, start_msg.message_id)


@router.message(Command("help"))
async def help_command(
    message: types.Message,
    state: FSMContext,
):
    await delete_old_messages(message.bot, message.chat.id, state)

    msg = await message.answer(
        "❓ <b>Помощь</b>\n\n"
        "Бот предназначен для подготовки к IT-собеседованиям.\n"
        "Доступные команды:\n"
        "— /menu — открыть главное меню\n"
        "— /progress — ваш прогресс\n"
        "— /buy — подписка PRO\n"
        "— /feedback — написать отзыв\n",
        parse_mode="HTML"
    )

    await message.delete()
    await save_message_id(state, msg.message_id)


@router.message(Command("about"))
async def about_command(
    message: types.Message,
    state: FSMContext,
):
    await delete_old_messages(message.bot, message.chat.id, state)

    msg =await message.answer(
        "ℹ️ <b>О боте</b>\n\n"
        "Этот бот создан для подготовки к IT-собеседованиям.\n"
        "Проект развивается с любовью ❤️\n\n"
        "Автор: @your_nickname",
        parse_mode="HTML"
    )

    await message.delete()
    await save_message_id(state, msg.message_id)


@router.message(Command("feedback"))
async def feedback_command(
    message: types.Message,
    state: FSMContext,
):
    await delete_old_messages(message.bot, message.chat.id, state)

    msg = await message.answer(
        "💬 <b>Обратная связь</b>\n\n"
        "Есть идеи или замечания?\n"
        "Напиши сюда: @your_feedback_bot или оставь отзыв прямо здесь.",
        parse_mode="HTML"
    )

    await message.delete()
    await save_message_id(state, msg.message_id)


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

    await query.message.delete()

    start_msg: types.Message = await query.message.bot.send_message(
        chat_id=query.message.chat.id,
        text=TEXT_MAIN_MENU,
        reply_markup=main_menu_kb,
        parse_mode="Markdown"
    )

    await state.update_data(start_msg_id=start_msg.message_id)
    await save_message_id(state, start_msg.message_id)
