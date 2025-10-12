from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

async def send_next_question(chat_id: int, state: FSMContext, bot):
    data = await state.get_data()
    current_q = data["current_q"]
    questions = data["questions"]

    if current_q >= len(questions):
        # Все вопросы пройдены
        await bot.send_message(chat_id, "🎉 Тест завершен! Посмотрите ваши результаты.")
        await state.clear()
        return

    question = questions[current_q]

    # Создаем inline-кнопки с вариантами ответов
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=opt, callback_data=f"answer:{i}") for i, opt in enumerate(question["options"])],
            [InlineKeyboardButton(text="↩️ Назад", callback_data="back")]
        ]
    )

    await bot.send_message(
        chat_id,
        f"Вопрос {current_q + 1}: {question['text']}",
        reply_markup=kb
    )
