from aiogram.fsm.context import FSMContext
from dependency_injector.wiring import inject, Provide

from bot.pkg.keyboards.exam import process_exam_kb
from bot.pkg.keyboards.test import result_test_kb
from bot.internal.services.v1 import SessionService, InterviewQuestionService
from bot.internal.services.v1 import Services as V1Services
from bot.utils import save_message_id
from bot.pkg.models import v1 as models

@inject
async def send_next_exam_question(
    chat_id: int,
    state: FSMContext,
    bot,
    message_id: int | None = None,
    session_service: SessionService = Provide[V1Services.session_service],
    interview_question_service: InterviewQuestionService = Provide[V1Services.interview_question_service]
):
    """
    Отправляет следующий вопрос экзамена пользователю или завершает экзамен, если вопросы закончились.
    """

    data = await state.get_data()
    current_q = data.get("current_q", 0)
    questions = data.get("questions", [])
    session_id = data.get("session_id")
    results = data.get("results", [])
    user_id = data.get("user_id")

    # ✅ Проверка завершения
    if current_q >= len(questions):
        correct = sum(1 for r in results if r.get("correct"))
        total = len(questions)
        percent = int((correct / total) * 100) if total else 0

        if session_id:
            cmd = models.SessionUpdateCommand(session_id=session_id, score=correct)
            await session_service.update_session(cmd)

        if message_id:
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception:
                pass

        text = (
            f"🧠 <b>Экзамен завершён!</b>\n\n"
            f"✅ Правильных ответов: <b>{correct}</b> из <b>{total}</b>\n"
            f"📊 Результат: <b>{percent}%</b>\n\n"
            f"Хочешь попробовать снова?"
        )

        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=result_test_kb,
            parse_mode="HTML",
        )
        await save_message_id(state, msg.message_id)
        await state.update_data(current_q=0, current_message_id=msg.message_id)
        return msg.message_id

    # ✅ Получаем текущий вопрос
    question = questions[current_q]
    question_text = question.get("title") if isinstance(question, dict) else question.title

    feedback = await interview_question_service.get_feedback_question(user_id, question.kb_question_id)

    text = f"📘 <b>Вопрос {current_q + 1}</b>\n\n{question_text}"

    # ✅ Формируем клавиатуру с учётом отметки mark
    print(feedback)
    keyboard = process_exam_kb(question, current_q, mark=feedback.mark)

    # ✅ Отображаем вопрос
    try:
        if message_id:
            await bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
        else:
            msg = await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
            message_id = msg.message_id
    except Exception:
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard,
            parse_mode="HTML",
        )
        message_id = msg.message_id

    # ✅ Обновляем состояние
    await state.update_data(
        current_q=current_q + 1,
        current_message_id=message_id,
    )

    return message_id
