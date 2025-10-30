from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🧠 Пройти тест"),
            KeyboardButton(text="🎯 Случайный вопрос"),
        ],
        [
            KeyboardButton(text="📚 Сборник вопросов"),
            KeyboardButton(text="🕐 Экзамен"),
        ],
        [
            KeyboardButton(text="👤 Личный кабинет"),
        ],
        [
        KeyboardButton(text="💎 Подписка"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери действие 👇",
)