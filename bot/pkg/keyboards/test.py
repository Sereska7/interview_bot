from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.pkg.models import v1 as models


icons = {
        "Python": "🐍",
        "SQL": "💾",
        "Алгоритмы": "💡",
        "Linux": "⚙️",
        "Docker": "🐳",
        "Git": "🌿",
        "FastAPI": "⚡",
        "Django": "🧩",
    }

def category_kb(categories: list[models.Category]) -> InlineKeyboardMarkup:
    """Создает инлайн-клавиатуру из списка категорий с эмодзи."""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    row = []
    for i, category in enumerate(categories, start=1):
        icon = icons.get(category.name, "📘")
        row.append(
            InlineKeyboardButton(
                text=f"{icon} {category.name}",
                callback_data=f"test_topic:{category.name}"
            )
        )

        if i % 2 == 0:
            keyboard.inline_keyboard.append(row)
            row = []

    if row:
        keyboard.inline_keyboard.append(row)

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="🏠 На главную", callback_data="back_main")
    ])

    return keyboard

result_test_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 На главную", callback_data="back_main")],
        [InlineKeyboardButton(text="🆕 Новый тест", callback_data="new_test")],
        [InlineKeyboardButton(text="📋 Разбор ответов", callback_data="view_answers")],
    ]
)
result_answers_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 На главную", callback_data="back_main")],
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
    buttons.append([InlineKeyboardButton(text="🏠 На главную", callback_data="back_main")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


empty_questions_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🧭 Выбрать другую тему", callback_data="retopic"),
            InlineKeyboardButton(text="⚡ Изменить уровень", callback_data="relevel"),
        ],
        [
            InlineKeyboardButton(text="↩️ Назад в раздел", callback_data="back_to_test_section"),
            InlineKeyboardButton(text="🏠 На главную", callback_data="back_main")
        ],
    ]
)


def summary_kb(topic: str, level: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Начать тест", callback_data=f"start_test:{topic}:{level}")],
        [
            InlineKeyboardButton(text="🧭 Выбрать другую тему", callback_data="retopic"),
            InlineKeyboardButton(text="⚡ Изменить уровень",   callback_data="relevel"),
        ],
        [
            InlineKeyboardButton(text="↩️ Назад в раздел", callback_data="back_to_test_section"),
            InlineKeyboardButton(text="🏠 На главную",     callback_data="back_main"),
        ],
    ])


def category_kb_return(categories: list[models.Category]) -> InlineKeyboardMarkup:
    """Создает клавиатуру выбора новой темы с эмодзи (режим возврата)."""

    kb = InlineKeyboardMarkup(inline_keyboard=[])
    row = []

    for i, c in enumerate(categories, start=1):
        icon = icons.get(c.name, "📘")
        row.append(
            InlineKeyboardButton(
                text=f"{icon} {c.name}",
                callback_data=f"retopic:{c.name}"
            )
        )

        if i % 2 == 0:
            kb.inline_keyboard.append(row)
            row = []

    if row:
        kb.inline_keyboard.append(row)

    kb.inline_keyboard.append([
        InlineKeyboardButton(text="↩️ Назад", callback_data="cancel_retopic")
    ])

    return kb


def level_keyboard_return(topic: str) -> InlineKeyboardMarkup:
    """Клавиатура выбора уровня, возвращающая обратно к резюме после выбора."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🧩 Junior", callback_data=f"level:{topic}:junior"),
            InlineKeyboardButton(text="⚙️ Middle", callback_data=f"level:{topic}:middle"),
            InlineKeyboardButton(text="🧠 Senior", callback_data=f"level:{topic}:senior")
        ],
        [
            InlineKeyboardButton(text="↩️ Назад", callback_data="cancel_relevel")
        ]
    ])
