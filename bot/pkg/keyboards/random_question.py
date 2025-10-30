from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Получить вопрос", callback_data="get_random_question")],
        [InlineKeyboardButton(text="📚 Выбрать тему", callback_data="choose_random_question_topic")],
        [InlineKeyboardButton(text="↩️ На главную", callback_data="back_main")]
    ])


next_question_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Следующий вопрос", callback_data="get_random_question")],
        [InlineKeyboardButton(text="↩️ На главную", callback_data="back_main")]
    ])


def process_question_kb(question) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=opt,callback_data=f"answer:{question.question_id}:{i}")]
        for i, opt in enumerate(question.options.values())
    ]

    buttons.append([InlineKeyboardButton(text="↩️ На главную", callback_data="back_main")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

