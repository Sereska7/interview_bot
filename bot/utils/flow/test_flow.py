from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

async def send_next_question(chat_id: int, state: FSMContext, bot, message_id: int = None):
    data = await state.get_data()
    current_q = data["current_q"]
    questions = data["questions"]

    if current_q >= len(questions):
        # Все вопросы пройдены
        if message_id:
            await bot.edit_message_text("🎉 Тест завершен! Посмотрите ваши результаты.", chat_id=chat_id, message_id=message_id)
        else:
            await bot.send_message(chat_id, "🎉 Тест завершен! Посмотрите ваши результаты.")
        await state.clear()
        return

    question = questions[current_q]

    # Создаем inline-кнопки (каждая кнопка в отдельной строке)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=opt, callback_data=f"answer:{i}")]
            for i, opt in enumerate(question.options.values())
        ] + [[InlineKeyboardButton(text="↩️ Назад", callback_data="back")]]
    )

    text = f"Вопрос {current_q + 1}: {question.question_text}"

    if message_id:
        # Редактируем существующее сообщение
        await bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=kb
        )
    else:
        # Отправляем новое сообщение
        msg = await bot.send_message(
            chat_id,
            text=text,
            reply_markup=kb
        )
        message_id = msg.message_id

    # Возвращаем message_id, чтобы следующий вопрос редактировал это же сообщение
    return message_id
