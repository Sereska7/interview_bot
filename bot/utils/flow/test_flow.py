from aiogram.fsm.context import FSMContext
from dependency_injector.wiring import inject, Provide

from bot.pkg.keyboards.test import result_test_kb, process_test_kb
from bot.internal.services.v1 import SessionService
from bot.internal.services.v1 import Services as V1Services
from bot.utils import save_message_id
from bot.pkg.models import v1 as models
from bot.utils.constants import format_test_result


@inject
async def send_next_question(
    chat_id: int,
    state: FSMContext,
    bot,
    message_id: int = None,
    session_service: SessionService = Provide[V1Services.session_service]
):
    """
    Отправляет следующий вопрос теста пользователю или завершает тест, если вопросы закончились.

    Args:
        chat_id (int): ID чата пользователя.
        state (FSMContext): Контекст состояний FSM для текущего пользователя.
        bot: Объект бота для отправки сообщений.
        message_id (int, optional): ID текущего сообщения с вопросом. Используется для редактирования.
        session_service (SessionService, optional): Сервис для работы с сессиями.

    Returns:
        int: ID сообщения с вопросом или результатом теста.
    """

    data = await state.get_data()
    current_q = data.get("current_q", 0)
    questions = data.get("questions", [])
    session_id = data.get("session_id")

    if current_q >= len(questions):
        results = data.get("results", [])
        correct_answers = sum(1 for r in results if r["correct"])
        total_questions = len(questions)

        if session_id:
            cmd = models.SessionUpdateCommand(
                session_id=session_id,
                score=correct_answers
            )
            await session_service.update_session(cmd)

        if message_id:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception:
                pass

        text = format_test_result(correct_answers, total_questions)
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=result_test_kb,
            parse_mode="HTML"
        )
        await save_message_id(state, msg.message_id)

        await state.update_data({
            "current_q": 0,
            "answers": [],
            "current_message_id": msg.message_id
        })

        return msg.message_id

    question = questions[current_q]

    if isinstance(question, dict):
        question_text = question.get("title") or question.get("text") or "Без текста"
    else:
        question_text = getattr(question, "title", "Без текста")

    text = f"📘 <b>Вопрос {current_q + 1}</b>\n\n{question_text}"

    if message_id:
        try:
            await bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=process_test_kb(question, current_q),
                parse_mode="MarkdownV2"
            )
        except Exception:
            msg = await bot.send_message(
                chat_id,
                text=text,
                reply_markup=process_test_kb(question, current_q),
                parse_mode="MarkdownV2"
            )
            message_id = msg.message_id
    else:
        msg = await bot.send_message(
            chat_id,
            text=text,
            reply_markup=process_test_kb(question, current_q),
            parse_mode="MarkdownV2"
        )
        message_id = msg.message_id

    await state.update_data(current_message_id=message_id)
    return message_id
