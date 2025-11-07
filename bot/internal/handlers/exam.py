from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dependency_injector.wiring import Provide, inject

from bot.internal.services.v1 import CategoryService, InterviewQuestionService, QuestionFeedbackService
from bot.internal.services.v1 import Services as V1Services
from bot.pkg.keyboards.exam import get_exam_keyboard
from bot.pkg.models.sql_models.question_feedback import FeedbackMark
from bot.pkg.states.exam_state import ExamStates
from bot.utils import delete_old_messages, save_message_id
from bot.utils.constants import EXAM_TEXT
from bot.utils.flow.exam_flow import send_next_exam_question

router = Router()

@router.message(F.text == "🕐 Экзамен")
@inject
async def exam_section(
    message: types.Message,
    state: FSMContext,
    category_service: CategoryService = Provide[V1Services.category_service]
):
    await delete_old_messages(message.bot, message.chat.id, state)
    await state.set_state(ExamStates.start)
    await message.delete()

    categories = await category_service.get_categories()
    await state.update_data(
        topics=categories,
        selected_topic=None,
        selected_level=None
    )

    msg = await message.answer(
        text=EXAM_TEXT,
        reply_markup=get_exam_keyboard(categories),
        parse_mode="HTML"
    )
    await (save_message_id(state, msg.message_id))


@router.callback_query(F.data.startswith("topic:"))
async def choose_topic(callback: types.CallbackQuery, state: FSMContext):
    topic = callback.data.split(":", 1)[1]
    data = await state.get_data()
    await state.update_data(
        selected_topic=topic,
    )

    await callback.message.edit_reply_markup(
        reply_markup=get_exam_keyboard(data["topics"], selected_topic=topic)
    )
    await callback.answer(f"Тема: {topic}")


@router.callback_query(F.data.startswith("level:"))
async def choose_grade(callback: types.CallbackQuery, state: FSMContext):
    level = callback.data.split(":", 1)[1]
    data = await state.get_data()
    await state.update_data(selected_level=level)

    await callback.message.edit_reply_markup(
        reply_markup=get_exam_keyboard(
            data["topics"],
            selected_topic=data.get("selected_topic"),
            selected_level=level
        )
    )
    await callback.answer(f"Уровень: {level}")


@router.callback_query(F.data == "start_exam")
@inject
async def start_exam(
    callback: types.CallbackQuery,
    state: FSMContext,
    interview_question_service: InterviewQuestionService = Provide[V1Services.interview_question_service]
):
    data = await state.get_data()
    topic = data.get("selected_topic")
    level = data.get("selected_level")
    user_id = data.get("user_id")

    await callback.message.edit_text(
        f"🧠 Начинаем экзамен!\n\n"
        f"Тема: <b>{topic}</b>\n"
        f"Уровень: <b>{level}</b>\n\n"
        f"Подготовка вопросов...",
        parse_mode="HTML"
    )

    questions = await interview_question_service.get_interview_question(topic, level, user_id)
    if not questions:
        await callback.message.edit_text(
            "⚠️ К сожалению, вопросов для этой темы пока нет.",
            parse_mode="HTML"
        )
        return

    await state.update_data(
        questions=questions,
        current_q=0,
        results=[],
    )

    await state.set_state(ExamStates.in_process)

    await send_next_exam_question(
        chat_id=callback.message.chat.id,
        state=state,
        bot=callback.message.bot
    )
