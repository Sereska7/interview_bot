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

def get_exam_keyboard(
    topics: list[models.Category],
    selected_topic: str | None = None,
    selected_level: str | None = None
) -> InlineKeyboardMarkup:
    """Создает клавиатуру выбора темы и грейда для экзамена."""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    row = []

    for i, topic in enumerate(topics, start=1):
        name = getattr(topic, "name", str(topic))
        icon = icons.get(name, "📘")
        text = f"✅ {icon} {name}" if name == selected_topic else f"{icon} {name}"

        row.append(InlineKeyboardButton(text=text, callback_data=f"topic:{name}"))

        if i % 2 == 0:
            keyboard.inline_keyboard.append(row)
            row = []

    if row:
        keyboard.inline_keyboard.append(row)

    text = "✅ 🎲 Без темы" if selected_topic == "Без темы" else "🎲 Без темы"
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=text, callback_data="topic:Без темы")
    ])

    grade_buttons = [
        InlineKeyboardButton(
            text="✅ 🧩 Junior" if selected_level == "Junior" else "🧩 Junior",
            callback_data="level:Junior"
        ),
        InlineKeyboardButton(
            text="✅ ⚙️ Middle" if selected_level == "Middle" else "⚙️ Middle",
            callback_data="level:Middle"
        ),
        InlineKeyboardButton(
            text="✅ 🧠 Senior" if selected_level == "Senior" else "🧠 Senior",
            callback_data="level:Senior"
        ),
    ]
    keyboard.inline_keyboard.append(grade_buttons)

    if selected_topic and selected_level:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text="▶ Начать экзамен", callback_data="start_exam")
        ])

    return keyboard


def process_exam_kb(
    question,
    question_index: int,
    mark: str | None = None,
) -> InlineKeyboardMarkup:
    """
    Универсальная клавиатура для экзамена.
    """

    # 🧠 Если mark — Enum, берём его значение
    if hasattr(mark, "value"):
        mark = mark.value

    def label(text: str, key: str) -> str:
        """Добавляет ✅ к выбранной отметке."""
        return f"✅ {text}" if mark == key else text

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    if isinstance(question, dict):
        options = question.get("options") or question.get("answers") or []
    else:
        options = getattr(question, "options", None) or getattr(question, "answers", None) or []

    if options:
        for option in options:
            option_text = option if isinstance(option, str) else str(option)
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text=option_text,
                    callback_data=f"exam_answer:{question_index}:{option_text}"
                )
            ])
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text="⏭ Пропустить",
                callback_data=f"skip_question:{question_index}"
            )
        ])

    # 🔹 Оценка сложности вопроса
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=label("🟢 Знаю", "know"), callback_data="exam_feedback:know"),
        InlineKeyboardButton(text=label("🟡 Сложно", "hard"), callback_data="exam_feedback:hard"),
        InlineKeyboardButton(text=label("🔴 Не знаю", "unknown"), callback_data="exam_feedback:unknown"),
    ])

    # 🔹 Остальные кнопки
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="📖 Развернутый ответ", callback_data="exam_show_detail")
    ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="💡 Примеры использования", callback_data="exam_show_examples")
    ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="⏭ Следующий вопрос", callback_data="exam_next_question"),
    ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="↩️ В раздел", callback_data="back_to_exam_section"),
        InlineKeyboardButton(text="🏠 На главную", callback_data="back_main"),
    ])

    return keyboard