
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dependency_injector.wiring import Provide, inject

from bot.internal.services.v1 import Services as V1Services
from bot.internal.handlers.start import handle_back
from bot.internal.keyboards.level import level_keyboard
from bot.internal.keyboards.test import keyboard_test, start_test_kb
from bot.internal.services.v1.question import QuestionService
from bot.internal.states.test_state import TestStates
from bot.pkg.models.sql_models.question import DifficultyLevel
from bot.utils.flow.test_flow import send_next_question
from bot.pkg.models import v1 as models

router = Router()


@router.message(F.text == "🧠 Пройти тест")
async def test_section(message: types.Message, state: FSMContext):
    data = await state.get_data()
    start_msg_id = data.get("start_msg_id")

    if start_msg_id:
        try:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=start_msg_id
            )
        except Exception:
            pass
    await state.set_state(TestStates.select_topic)
    await message.delete()

    await message.answer(
        "🧠 <b>Раздел: Тесты</b>\n\n"
        "Выберите тему, по которой хотите пройти тест:",
        reply_markup=keyboard_test,
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("test_topic:"))
async def handle_topic_choice(
    query: CallbackQuery,
    state: FSMContext
):
    topic = query.data.split(":")[1]

    if topic == "back":
        await handle_back(query, state)
        return

    await state.update_data(topic=topic, current_q=0, answers=[])
    await state.set_state(TestStates.in_progress)

    await query.message.edit_text(
        f"✅ Вы выбрали тему: <b>{topic.capitalize()}</b>\n\n"
        "Выберите уровень сложности:",
        reply_markup=level_keyboard(topic),
        parse_mode="HTML"
    )
    await query.answer()


@router.callback_query(F.data.startswith("level:"))
async def handle_level_choice(query: CallbackQuery, state: FSMContext):
    _, topic, level = query.data.split(":")

    await state.update_data(level=level, topic=topic, current_q=1, answers=[])

    await state.set_state(TestStates.ready_to_start)

    await query.message.edit_text(
        f"✅ Тема: <b>{topic.capitalize()}</b>\n"
        f"⚡ Уровень: <b>{level.capitalize()}</b>\n\n"
        "Нажмите кнопку ниже, чтобы начать тест:",
        reply_markup=start_test_kb(topic, level),
        parse_mode="HTML"
    )

    await query.answer()


@router.callback_query(F.data.startswith("start_test:"), StateFilter(TestStates.ready_to_start))
@inject
async def start_test(
    query: CallbackQuery,
    state: FSMContext,
    question_service: QuestionService = Provide[V1Services.question_service]
):

    _, topic, level = query.data.split(":")

    await query.message.delete()

    # Получаем 10 вопросов из базы по теме и уровню
    cmd = models.QuestionReadCommand(
        category=topic.capitalize(),
        difficulty=DifficultyLevel[level.upper()],
        limit=10
    )
    questions = await question_service.get_questions(cmd)

    if not questions:
        await query.message.edit_text("❌ К сожалению, вопросы для этой темы/уровня не найдены.")
        await state.clear()
        await query.answer()
        return

    # Сохраняем вопросы и текущее положение в FSM
    await state.update_data(
        topic=topic,
        level=level,
        questions=questions,
        current_q=0,
        answers=[]
    )

    # Устанавливаем состояние "в процессе теста"
    await state.set_state(TestStates.in_progress)

    # Отправляем первый вопрос
    await send_next_question(query.message.chat.id, state, query.message.bot)

    await query.answer()


@router.callback_query(F.data.startswith("answer:"), StateFilter(TestStates.in_progress))
async def process_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_q = data["current_q"]
    questions = data["questions"]
    question = questions[current_q]

    selected_index = int(callback.data.split(":")[1])
    selected_key = list(question.options.keys())[selected_index]

    correct = selected_key == question.correct_option

    results = data.get("results", [])
    results.append({"question_id": question.id, "correct": correct})
    await state.update_data(results=results, current_q=current_q + 1)

    await callback.answer("Ответ принят ✅")

    # Редактируем сообщение текущим вопросом
    message_id = callback.message.message_id
    await send_next_question(callback.message.chat.id, state, callback.message.bot, message_id=message_id)
