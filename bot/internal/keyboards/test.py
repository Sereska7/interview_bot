from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🐍 Python", callback_data="test_topic:python"),
            InlineKeyboardButton(text="💾 SQL", callback_data="test_topic:sql")
        ],
        [
            InlineKeyboardButton(text="💡 Алгоритмы", callback_data="test_topic:algorithms"),
            InlineKeyboardButton(text="⚙️ Linux", callback_data="test_topic:linux")
        ],
        [
            InlineKeyboardButton(text="↩️ Назад", callback_data="back")
        ]
    ])

def start_test_kb(topic: str, level:str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="▶️ Начать тест", callback_data=f"start_test:{topic}:{level}")],
                [InlineKeyboardButton(text="↩️ Назад", callback_data="back")]
            ]
        )