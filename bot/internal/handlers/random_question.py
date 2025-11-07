
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dependency_injector.wiring import inject, Provide

from bot.internal.services.v1 import InterviewQuestionService
from bot.internal.services.v1 import Services as V1Services
from bot.internal.services.v1.question_feedback import QuestionFeedbackService
from bot.pkg.keyboards.random_question import keyboard, \
    process_question_kb_with_feedback, show_answer_kb_with_feedback, no_unknown_questions_kb
from bot.pkg.models.sql_models.question_feedback import FeedbackMark
from bot.pkg.states.random_question_state import RQStates
from bot.utils import delete_old_messages, save_message_id
from bot.utils.constants import RQ_TEXT
from bot.pkg.models import v1 as models

router = Router()

@router.message(F.text == "🎲 Случайный вопрос")
async def random_question_section(
    message: types.Message,
    state: FSMContext,
):
    """"""

    await delete_old_messages(message.bot, message.chat.id, state)
    await message.delete()
    await state.set_state(RQStates.start)

    msg = await message.answer(
        RQ_TEXT,
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await save_message_id(state, msg.message_id)


@router.callback_query(F.data == "back_to_random_section")
async def back_to_random_section(callback: CallbackQuery, state: FSMContext):
    """Возврат в раздел случайных вопросов."""

    await state.set_state(RQStates.start)
    await callback.message.edit_text(
        RQ_TEXT,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@router.callback_query(F.data == "get_random_question", StateFilter(RQStates.start, RQStates.in_process))
@inject
async def get_random_question(
    callback: CallbackQuery,
    state: FSMContext,
    interview_question_service: InterviewQuestionService = Provide[V1Services.interview_question_service]
):
    """Выдаёт случайный вопрос с учётом сложности и отметки пользователя."""

    await state.set_state(RQStates.in_process)

    data = await state.get_data()
    last_questions: list[int] = data.get("last_questions", [])
    user_id = data.get("user_id")

    query = models.InterviewQuestionReadQuery(
        user_id=user_id,
        last_questions=last_questions,
        difficulty=data.get("current_grade"),
    )

    question, feedback = await interview_question_service.get_random_question(query)
    if not question:
        await callback.message.edit_text("❌ Вопросы не найдены.")
        return

    last_questions.append(question.kb_question_id)
    if len(last_questions) > 4:
        last_questions.pop(0)
    await state.update_data(
        question=question,
        last_questions=last_questions,
        feedback_mark=feedback.mark if feedback else None,
        mode="random",
    )

    await callback.message.edit_text(
        text=f"🎯 <b>Вопрос:</b>\n\n{question.title}",
        reply_markup=await process_question_kb_with_feedback(
            state
        ),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "get_unknown_question", StateFilter(RQStates.start, RQStates.in_process))
@inject
async def get_unknown_question(
    callback: CallbackQuery,
    state: FSMContext,
    interview_question_service: InterviewQuestionService = Provide[V1Services.interview_question_service]
):
    """"""
    await state.set_state(RQStates.in_process)

    data = await state.get_data()
    user_id = data.get("user_id")
    last_questions: list[int] = data.get("last_questions", [])

    question, feedback = await interview_question_service.get_unknown_question(
        user_id=user_id,
        last_questions=last_questions
    )
    if not question:
        await state.update_data(last_questions=[])
        await callback.message.edit_text(
            text=(
                "⚠️ Все вопросы, отмеченные как <b>«не знаю»</b>, "
                "уже были показаны.\n\n"
                "Вы можете пройти их заново или перейти к новым вопросам 👇"
            ),
            reply_markup=no_unknown_questions_kb,
            parse_mode="HTML",
        )
        return

    last_questions.append(question.kb_question_id)
    if len(last_questions) > 2:
        last_questions.pop(0)

    await state.update_data(
        question=question,
        last_questions=last_questions,
        feedback_mark=feedback.mark if feedback else None,
        mode="unknown",
    )

    await callback.message.edit_text(
        text=f"🎯 <b>Вопрос:</b>\n\n{question.title}",
        reply_markup=await process_question_kb_with_feedback(
            state
        ),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "restart_unknown_questions")
async def restart_unknown_questions(callback: CallbackQuery, state: FSMContext):
    """Сбрасывает просмотренные вопросы и запускает повтор 'не знаю'."""

    await state.update_data(last_questions=[])
    await callback.answer("🔄 Повтор вопросов 'не знаю' запущен!")
    await get_unknown_question(callback, state)


@router.callback_query(F.data == "show_response", StateFilter(RQStates.in_process))
async def handle_answer(
    callback: CallbackQuery,
    state: FSMContext,
):
    """"""

    await state.set_state(RQStates.showing_answer)
    data = await state.get_data()
    question = data.get("question")
    feedback_mark = data.get("feedback_mark")

    text = (
        f"🎯 <b>Вопрос:</b>\n"
        f"{question.title}\n\n"
        f"📘 <b>Краткий ответ:</b>\n"
        f"{question.short_answer}"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=show_answer_kb_with_feedback(feedback_mark),
        parse_mode="HTML",
    )
    await state.update_data(current_keyboard="answer")


@router.callback_query(F.data == "show_detail_answer", StateFilter(RQStates.showing_answer))
async def show_detail_answer(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(RQStates.showing_answer)
    data = await state.get_data()
    question = data.get("question")
    feedback_mark = data.get("feedback_mark")

    text = (
        f"🎯 <b>Вопрос:</b>\n"
        f"{question.title}\n\n"
        f"📘 <b>Краткий ответ:</b>\n"
        f"{question.short_answer}\n\n"
        f"📖 <b>Развернутый ответ</b>\n"
        f"{question.detailed_answer}"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=show_answer_kb_with_feedback(feedback_mark),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "show_examples_answer", StateFilter(RQStates.showing_answer))
async def show_detail_answer(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(RQStates.showing_answer)
    data = await state.get_data()
    question = data.get("question")
    feedback_mark = data.get("feedback_mark")

    text = (
        f"🎯 <b>Вопрос:</b>\n"
        f"{question.title}\n\n"
        f"📘 <b>Краткий ответ:</b>\n"
        f"{question.short_answer}\n\n"
        f"📖 <b>Развернутый ответ:</b>\n"
        f"{question.detailed_answer}\n\n"
        f"💡 <b>Примеры использования</b>:\n"
        f"{question.examples}"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=show_answer_kb_with_feedback(feedback_mark),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("difficulty_"))
@inject
async def handle_difficulty(
    callback: CallbackQuery,
    state: FSMContext,
    question_feedback_service: QuestionFeedbackService = Provide[V1Services.question_feedback_service]
):
    data = await state.get_data()
    user_id = data.get("user_id")
    question = data.get("question")
    current_keyboard = data.get("current_keyboard")

    if not question or not user_id:
        await callback.answer("⚠️ Не удалось определить вопрос.", show_alert=True)
        return

    data_suffix = callback.data.replace("difficulty_", "")
    mark = FeedbackMark(data_suffix)

    cmd = models.QuestionFeedbackCreateCommand(
        user_id=user_id,
        question_id=question.kb_question_id,
        mark=mark,
    )
    feedback = await question_feedback_service.create_feedback(cmd)

    await state.update_data(
        feedback_mark=feedback.mark if feedback else None,
    )
    if current_keyboard == "answer":
        print(show_answer_kb_with_feedback)
        new_kb = show_answer_kb_with_feedback(mark)
    else:
        print(process_question_kb_with_feedback)
        new_kb = await process_question_kb_with_feedback(state)

    feedback_labels = {
        FeedbackMark.KNOW: "🟢 Знаю",
        FeedbackMark.HARD: "🟡 Сложно",
        FeedbackMark.UNKNOWN: "🔴 Не знаю",
    }

    await callback.answer(f"✅ Оценка сохранена: {feedback_labels[mark]}")
    await callback.message.edit_reply_markup(reply_markup=new_kb)


@router.callback_query(F.data == "back_to_answer")
async def back_to_short_answer(
    callback: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(RQStates.in_process)

    data = await state.get_data()
    question = data.get("question")
    await state.update_data(current_keyboard="process")

    if not question:
        await callback.answer("⚠️ Вопрос не найден.")
        return

    await callback.message.edit_text(
        text=f"🎯 <b>Вопрос:</b>\n\n{question.title}",
        reply_markup=await process_question_kb_with_feedback(
            state
        ),
        parse_mode="HTML",
    )

