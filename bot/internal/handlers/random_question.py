
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dependency_injector.wiring import inject, Provide

from bot.internal.services.v1 import QuestionService, ResultService, SessionService, UserService
from bot.internal.services.v1 import Services as V1Services
from bot.pkg.keyboards.random_question import keyboard, process_question_kb, next_question_kb
from bot.pkg.states.random_question_state import RQStates
from bot.utils import delete_old_messages, save_message_id
from bot.utils.constants import RQ_TEXT, escape_html
from bot.pkg.models import v1 as models

router = Router()

@router.message(F.text == "🎯 Случайный вопрос")
@inject
async def random_question_section(
    message: types.Message,
    state: FSMContext,
    user_service: UserService = Provide[V1Services.user_service]
):
    """"""

    data = await state.get_data()
    user_id = data.get("user_id")
    if not user_id:
        user = await user_service.get_by_telegram_id(message.from_user.id)
        await state.update_data(user_id=user.user_id)

    await delete_old_messages(message.bot, message.chat.id, state)
    await message.delete()

    msg = await message.answer(RQ_TEXT, reply_markup=keyboard)
    await save_message_id(state, msg.message_id)


@router.callback_query(F.data == "get_random_question")
@inject
async def get_random_question(
    callback: CallbackQuery,
    state: FSMContext,
    question_service: QuestionService = Provide[V1Services.question_service]
):
    """"""
    await state.set_state(RQStates.in_progress)

    data = await state.get_data()
    last_questions: list[int] = data.get("last_questions", [])

    question = await question_service.get_random_question(last_questions)
    if not question:
        await callback.message.edit_text("❌ Вопросы не найдены.")
        return

    last_questions.append(question.question_id)
    if len(last_questions) > 5:
        last_questions.pop(0)
    await state.update_data(
        question=question,
        last_questions=last_questions
    )

    await callback.message.edit_text(
        text=f"🎯 Вопрос:\n\n{question.question_text}",
        reply_markup=process_question_kb(question)
    )


@router.callback_query(F.data.startswith("answer:"), StateFilter(RQStates.in_progress))
@inject
async def handle_answer(
    callback: CallbackQuery,
    state: FSMContext,
    result_service: ResultService = Provide[V1Services.result_service],
    session_service: SessionService = Provide[V1Services.session_service]
):
    """
    """

    data = await state.get_data()
    question = data.get("question")
    user_id = data.get("user_id")

    try:
        _, selected_index = callback.data.split(":")
        selected_index = int(selected_index)

        selected_key = list(question.options.keys())[selected_index]
    except ValueError:
        await callback.answer("⚠️ Ошибка данных кнопки", show_alert=True)
        return

    correct_key = question.correct_option
    is_correct = selected_key == correct_key

    cmd = models.ResultCreateCommand(
        user_id=user_id,
        session_id=None,
        question_id=question.question_id,
        chosen_option=selected_key,
        is_correct=is_correct
    )
    await result_service.create_result(cmd)

    chosen_text = question.options[selected_key]
    correct_text = question.options[correct_key]

    if is_correct:
        result_text = (
            f"✅ <b>Правильно!</b>\n\n"
            f"<i>{escape_html(question.question_text)}</i>\n\n"
            f"Твой ответ: <b>{escape_html(chosen_text)}</b>"
        )
    else:
        result_text = (
            f"❌ <b>Неправильно.</b>\n\n"
            f"<i>{escape_html(question.question_text)}</i>\n\n"
            f"Твой ответ: <b>{escape_html(chosen_text)}</b>\n"
            f"Правильный ответ: <b>{escape_html(correct_text)}</b>"
        )

    await callback.message.edit_text(
        text=result_text,
        reply_markup=next_question_kb,
        parse_mode="HTML"
    )
