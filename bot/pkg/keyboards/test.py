from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🐍 Python", callback_data="test_topic:python"),
            InlineKeyboardButton(text="💾 SQL", callback_data="test_topic:sql")
        ],
        [
            InlineKeyboardButton(text="💡 Алгоритмы", callback_data="test_topic:Алгоритмы"),
            InlineKeyboardButton(text="⚙️ Linux", callback_data="test_topic:linux")
        ],
        [
            InlineKeyboardButton(text="↩️ На главную", callback_data="back_main")
        ]
    ])

result_test_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="↩️ На главную", callback_data="back_main")],
        [InlineKeyboardButton(text="🆕 Новый тест", callback_data="new_test")],
        [InlineKeyboardButton(text="📋 Разбор ответов", callback_data="view_answers")],
    ]
)
result_answers_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="↩️ На главную", callback_data="back_main")],
        [InlineKeyboardButton(text="🔄 Пройти ещё раз", callback_data="retry_test")],
    ]
)

def start_test_kb(topic: str, level:str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="▶️ Начать тест", callback_data=f"start_test:{topic}:{level}")],
                [InlineKeyboardButton(text="↩️ Назад", callback_data=f"start_test:{topic}:back")]
            ]
        )


def process_test_kb(question, current_q: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=opt, callback_data=f"answer:{current_q}:{i}")]
        for i, opt in enumerate(question.options.values())
    ]
    buttons.append([InlineKeyboardButton(text="↩️ На главную", callback_data="back_main")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
