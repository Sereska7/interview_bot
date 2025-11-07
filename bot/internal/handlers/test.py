from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dependency_injector.wiring import Provide, inject

from bot.internal.services.v1 import Services as V1Services
from bot.internal.handlers.start import handle_back
from bot.pkg.keyboards.level import level_keyboard
from bot.pkg.keyboards.test import category_kb, start_test_kb, result_answers_kb, summary_kb, category_kb_return, \
    level_keyboard_return
from bot.internal.services.v1.question import QuestionService
from bot.internal.services.v1.result import ResultService
from bot.internal.services.v1.session import SessionService
from bot.internal.services.v1.category import CategoryService
from bot.pkg.states.test_state import TestStates
from bot.utils.constants import TEST_TEXT, test_topic, format_test_result_detailed, summary_text
from bot.utils.flow.test_flow import send_next_question
from bot.pkg.models import v1 as models
from bot.utils import delete_old_messages, save_message_id


router = Router()


@router.message(F.text == "🧠 Пройти тест")
@inject
async def test_section(
    message: types.Message,
    state: FSMContext,
    category_service: CategoryService = Provide[V1Services.category_service],
):
    """
    Обрабатывает нажатие кнопки '🧠 Пройти тест' и переводит пользователя в раздел тестов.

    Args:
        message (types.Message): Объект входящего сообщения от Telegram.
        state (FSMContext): Контекст состояний FSM для текущего пользователя.

    Returns:
        None: Очищает старые сообщения, устанавливает состояние выбора темы,
        отправляет сообщение с клавиатурой выбора теста и сохраняет message_id.
    """

    await delete_old_messages(message.bot, message.chat.id, state)
    await state.set_state(TestStates.select_topic)
    await message.delete()

    categories = await category_service.get_categories()
    await state.update_data(categories=categories)

    msg = await message.answer(
        text=TEST_TEXT,
        reply_markup=category_kb(categories),
        parse_mode="HTML"
    )
    await save_message_id(state, msg.message_id)


@router.callback_query(F.data == "retopic")
async def handle_retopic_entry(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    categories = data.get("categories")

    await state.set_state(TestStates.select_topic)
    await callback.message.edit_text(
        text="📘 Выберите новую тему:",
        reply_markup=category_kb_return(categories),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("retopic:"))
async def handle_retopic_choose(callback: CallbackQuery, state: FSMContext):
    _, new_topic = callback.data.split(":", 1)
    data = await state.get_data()
    level = data.get("level")

    await state.update_data(topic=new_topic)
    await state.set_state(TestStates.ready_to_start)

    await callback.message.edit_text(
        text=summary_text(new_topic, level),
        reply_markup=summary_kb(new_topic, level),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("cancel_retopic"))
async def handle_cancel_retopic_entry(callback: CallbackQuery, state: FSMContext):
    """"""

    data = await state.get_data()
    topic = data.get("topic")
    level = data.get("level")

    await callback.message.edit_text(
        text=summary_text(topic, level),
        reply_markup=summary_kb(topic, level),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "relevel")
async def handle_relevel_entry(callback: CallbackQuery, state: FSMContext):
    """
    ⚡ Обрабатывает выбор нового уровня сложности.
    Показывает клавиатуру уровней, после выбора возвращает к экрану-резюме.
    """
    data = await state.get_data()
    topic = data.get("topic")

    await state.set_state(TestStates.select_level)
    await callback.message.edit_text(
        text=f"⚡ Выберите новый уровень сложности для темы <b>{topic}</b>:",
        reply_markup=level_keyboard_return(topic),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("relevel:"))
async def handle_relevel_choose(callback: CallbackQuery, state: FSMContext):
    """
    После выбора нового уровня — возвращаемся к экрану-резюме.
    """
    _, topic, level = callback.data.split(":")
    await state.update_data(level=level)

    await state.set_state(TestStates.ready_to_start)
    await callback.message.edit_text(
        text=summary_text(topic, level),
        reply_markup=summary_kb(topic, level),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("cancel_relevel"))
async def handle_cancel_relevel_entry(callback: CallbackQuery, state: FSMContext):
    """"""

    data = await state.get_data()
    topic = data.get("topic")
    level = data.get("level")

    await callback.message.edit_text(
        text=summary_text(topic, level),
        reply_markup=summary_kb(topic, level),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("test_topic:"), StateFilter(TestStates.select_topic))
async def handle_topic_choice(
    callback: CallbackQuery,
    state: FSMContext
):
    """
    Обрабатывает выбор темы пользователем при нажатии кнопки теста.

    Args:
        callback (CallbackQuery): Объект callback запроса от Telegram.
        state (FSMContext): Контекст состояний FSM для текущего пользователя.

    Returns:
        None: Сохраняет выбранную тему в состояние, сбрасывает текущий номер вопроса и ответы,
        переводит пользователя на выбор уровня сложности и редактирует сообщение с клавиатурой.
    """

    topic = callback.data.split(":")[1]

    if topic == "back":
        await handle_back(callback, state)
        return

    await state.update_data(topic=topic, current_q=0, answers=[])
    await state.set_state(TestStates.select_level)

    await callback.message.edit_text(
        text=test_topic(topic),
        reply_markup=level_keyboard(topic),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("level:"), StateFilter(TestStates.select_level))
async def handle_level_choice(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает выбор уровня сложности пользователем при нажатии кнопки.

    Args:
        callback (CallbackQuery): Объект callback запроса от Telegram.
        state (FSMContext): Контекст состояний FSM для текущего пользователя.

    Returns:
        None: Сохраняет выбранный уровень и тему в состояние, сбрасывает текущий номер вопроса и ответы,
        переводит пользователя в состояние готовности к старту теста, редактирует сообщение с клавиатурой.
        Если выбран "back", возвращает пользователя к выбору темы.
    """

    _, topic, level = callback.data.split(":")

    data = await state.get_data()
    categories = data.get("categories")


    if level == "back":
        await state.set_state(TestStates.select_topic)
        await callback.message.edit_text(
            text=test_topic(topic),
            reply_markup=category_kb(categories),
            parse_mode="HTML"
        )
        return

    await state.update_data(level=level, topic=topic, current_q=1, answers=[])
    await state.set_state(TestStates.ready_to_start)

    await callback.message.edit_text(
        text=summary_text(topic, level),
        reply_markup=summary_kb(topic, level),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("start_test:"), StateFilter(TestStates.ready_to_start))
@inject
async def start_test(
    callback: CallbackQuery,
    state: FSMContext,
    question_service: QuestionService = Provide[V1Services.question_service],
    session_service: SessionService = Provide[V1Services.session_service],
):
    """
    Обрабатывает нажатие кнопки 'Начать тест' и запускает тестирование пользователя.

    Args:
        callback (CallbackQuery): Объект callback запроса от Telegram.
        state (FSMContext): Контекст состояний FSM для текущего пользователя.
        question_service (QuestionService): Сервис для получения вопросов.
        session_service (SessionService): Сервис для создания сессий.

    Returns:
        None: Получает вопросы из базы, создаёт новую сессию, сохраняет все данные в FSM,
        переводит пользователя в состояние прохождения теста и отправляет первый вопрос.
        Если выбран "back", возвращает пользователя к выбору уровня.
    """

    _, topic, level = callback.data.split(":")

    if level == "back":
        await state.set_state(TestStates.select_level)
        await callback.message.edit_text(
            text=test_topic(topic),
            reply_markup=level_keyboard(topic),
            parse_mode="HTML"
        )
        return

    questions = await question_service.get_questions_or_alert(
        topic, level, callback.message.chat.id, state, callback
    )
    if not questions:
        await callback.answer()
        return

    data = await state.get_data()
    user_id = data.get("user_id")
    cmd = models.SessionCreateCommand(
        user_id=user_id,
        category=topic.capitalize()
    )
    new_session = await session_service.create_session(cmd)

    await state.update_data(
        topic=topic,
        level=level,
        questions=questions,
        session_id=new_session.session_id,
        current_q=0,
        answers=[]
    )

    await state.set_state(TestStates.in_progress)
    await send_next_question(callback.message.chat.id, state, callback.message.bot)


@router.callback_query(F.data.startswith("answer:"), StateFilter(TestStates.in_progress))
@inject
async def process_answer(
    callback: CallbackQuery,
    state: FSMContext,
    result_service: ResultService = Provide[V1Services.result_service]
):
    """
    Обрабатывает выбранный пользователем ответ на текущий вопрос теста.

    Args:
        callback (CallbackQuery): Объект callback запроса от Telegram.
        state (FSMContext): Контекст состояний FSM для текущего пользователя.
        result_service (ResultService): Сервис для сохранения результатов ответов.

    Returns:
        None: Сохраняет результат в базу, обновляет FSM и отправляет следующий вопрос пользователю.
    """

    data = await state.get_data()
    questions = data.get("questions", [])
    current_q = data.get("current_q", 0)

    try:
        question_index = int(callback.data.split(":")[1])
        selected_index = int(callback.data.split(":")[2])
        question = questions[question_index]
        selected_key = list(question.options.keys())[selected_index]
    except (IndexError, ValueError, KeyError):
        await callback.answer("Некорректный выбор.", show_alert=True)
        return

    correct = selected_key == question.correct_option

    user_id = data.get("user_id")
    session_id = data.get("session_id")
    cmd = models.ResultCreateCommand(
        user_id=user_id,
        question_id=question.question_id,
        session_id=session_id,
        chosen_option=selected_key,
        is_correct=correct
    )
    await result_service.create_result(cmd)

    results = data.get("results", [])
    results.append({"question_id": question.question_id, "correct": correct})
    await state.update_data(results=results, current_q=current_q + 1)

    await callback.answer("Ответ принят ✅")

    message_id = data.get("current_message_id")
    try:
        new_message_id = await send_next_question(
            callback.message.chat.id,
            state,
            callback.message.bot,
            message_id=message_id
        )
        await state.update_data(current_message_id=new_message_id)
    except Exception:
        await callback.answer("Ошибка при отправке следующего вопроса.", show_alert=True)



@router.callback_query(F.data == "view_answers")
@inject
async def view_answers(
    callback: CallbackQuery,
    state: FSMContext,
    result_service: ResultService = Provide[V1Services.result_service]
):
    """
    Отображает пользователю разбор его ответов на тест.

    Args:
        callback (CallbackQuery): Объект callback запроса от Telegram.
        state (FSMContext): Контекст состояний FSM для текущего пользователя.
        result_service (ResultService): Сервис для получения результатов теста.

    Returns:
        None: Формирует сообщение с результатами и разбором ошибок, редактирует текущее сообщение.
    """

    data = await state.get_data()
    session_id = data.get("session_id")
    if not session_id:
        await callback.answer("Ошибка: session_id не найден.", show_alert=True)
        return

    results = await result_service.get_results_by_session(session_id)
    if not results:
        await callback.answer("Результаты не найдены.", show_alert=True)
        return

    correct_count = sum(1 for r in results if r.is_correct)
    total = len(results)

    text = format_test_result_detailed(results, correct_count, total)

    await callback.message.edit_text(
        text=text.strip(),
        parse_mode="HTML",
        reply_markup=result_answers_kb
    )



@router.callback_query(F.data == "new_test")
@inject
async def new_test(
    callback: CallbackQuery,
    state: FSMContext,
    session_service: SessionService = Provide[V1Services.session_service],
    question_service: QuestionService = Provide[V1Services.question_service],
):
    """
    Запускает новый тест с теми же параметрами темы и уровня, создаёт новую сессию
    и отправляет пользователю первый вопрос.

    Args:
        callback (CallbackQuery): Объект callback запроса от Telegram.
        state (FSMContext): Контекст состояний FSM для текущего пользователя.
        session_service (SessionService): Сервис для работы с сессиями.
        question_service (QuestionService): Сервис для получения вопросов.

    Returns:
        None: Создаёт новую сессию, получает вопросы, обновляет данные FSM,
        удаляет старое сообщение и отправляет первый вопрос теста.
        Если вопросы не найдены — уведомляет пользователя.
    """

    data = await state.get_data()
    user_id = data.get("user_id")
    topic = data.get("topic")
    level = data.get("level")

    cmd = models.SessionCreateCommand(
        user_id=user_id,
        category=topic.capitalize()
    )
    new_session = await session_service.create_session(cmd)

    questions = await question_service.get_questions_or_alert(
        topic, level, callback.message.chat.id, state, callback.bot
    )
    if not questions:
        await callback.answer()
        return

    await state.update_data(
        session_id=new_session.session_id,
        questions=questions,
        current_q=0,
        results=[]
    )

    if callback.message:
        try:
            await callback.message.delete()
        except Exception:
            pass

    new_message_id = await send_next_question(
        chat_id=callback.from_user.id,
        state=state,
        bot=callback.bot
    )
    await state.update_data(current_message_id=new_message_id)
    await callback.answer()


@router.callback_query(F.data == "retry_test")
@inject
async def retry_test(
    callback: CallbackQuery,
    state: FSMContext,
    session_service: SessionService = Provide[V1Services.session_service],
):
    """
    Обрабатывает нажатие кнопки 'Пройти ещё раз' и перезапускает тест пользователя.

    Args:
        callback (CallbackQuery): Callback-запрос от Telegram.
        state (FSMContext): Контекст состояний FSM для пользователя.
        session_service (SessionService): Сервис для создания новой сессии.

    Returns:
        None: Создаёт новую сессию, сбрасывает прогресс в FSM, удаляет старое сообщение
        и отправляет первый вопрос нового теста.
    """
    data = await state.get_data()
    questions = data.get("questions")
    user_id = data.get("user_id")
    topic = data.get("topic")

    if not questions:
        await callback.answer("Нет вопросов для повторного прохождения.", show_alert=True)
        return

    cmd = models.SessionCreateCommand(
        user_id=user_id,
        category=topic.capitalize()
    )
    new_session = await session_service.create_session(cmd)

    await state.update_data(
        session_id=new_session.session_id,
        questions=questions,
        current_q=0,
        results=[]
    )

    if callback.message:
        await callback.message.delete()

    new_message_id = await send_next_question(
        chat_id=callback.from_user.id,
        state=state,
        bot=callback.bot
    )

    await state.update_data(current_message_id=new_message_id)

    await callback.answer()


@router.callback_query(F.data == "back_to_test_section")
async def back_to_test_section(callback: CallbackQuery, state: FSMContext):
    """Возврат в раздел тест."""

    await state.set_state(TestStates.select_topic)
    data = await state.get_data()
    categories = data.get("categories")

    await callback.message.edit_text(
        text=TEST_TEXT,
        reply_markup=category_kb(categories),
        parse_mode="HTML"
    )

#TODO
# Подумать над наполненностью раздела ТЕСТ