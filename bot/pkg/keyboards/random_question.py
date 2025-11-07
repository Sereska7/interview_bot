from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.pkg.models.sql_models.question_feedback import FeedbackMark

keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Случайный вопрос", callback_data="get_random_question")],
        [InlineKeyboardButton(text="❓ Из категории “Не знаю”", callback_data="get_unknown_question")],
        [InlineKeyboardButton(text="🏠 На главную", callback_data="back_main")]
    ])


no_unknown_questions_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔄 Пройти заново",
                callback_data="restart_unknown_questions"
            )
        ],
        [
            InlineKeyboardButton(
                text="🎯 Случайный вопрос",
                callback_data="get_random_question"
            )
        ],
        [
            InlineKeyboardButton(text="↩️ Назад в раздел", callback_data="back_to_random_section"),
            InlineKeyboardButton(text="🏠 На главную", callback_data="back_main")
        ],
    ]
)


async def process_question_kb_with_feedback(
    state: FSMContext,
) -> InlineKeyboardMarkup:
    """Создаёт клавиатуру вопроса с отметкой выбранной сложности."""

    data = await state.get_data()
    mark = data.get("feedback_mark")
    mode = data.get("mode")

    def label(text: str, key: str) -> str:
        return f"✅ {text}" if mark == key else text

    next_callback = "get_unknown_question" if mode == "unknown" else "get_random_question"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=label("🟢 Знаю", "know"),
                    callback_data="difficulty_know"
                ),
                InlineKeyboardButton(
                    text=label("🟡 Сложно", "hard"),
                    callback_data="difficulty_hard"
                ),
                InlineKeyboardButton(
                    text=label("🔴 Не знаю", "unknown"),
                    callback_data="difficulty_unknown"
                ),
            ],
            [InlineKeyboardButton(text="👁 Показать ответ", callback_data="show_response")],
            [InlineKeyboardButton(text="🎯 Следующий вопрос", callback_data=next_callback)],
            [
                InlineKeyboardButton(text="↩️ Назад в раздел", callback_data="back_to_random_section"),
                InlineKeyboardButton(text="🏠 На главную", callback_data="back_main")
            ],
        ]
    )

def show_answer_kb_with_feedback(mark: Optional[str] = None) -> InlineKeyboardMarkup:
    """Клавиатура для краткого ответа, с отметкой выбранной сложности."""

    def label(text: str, key: str) -> str:
        return f"✅ {text}" if mark == key else text

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=label("🟢 Знаю", "know"), callback_data="difficulty_know"),
                InlineKeyboardButton(text=label("🟡 Сложно", "hard"), callback_data="difficulty_hard"),
                InlineKeyboardButton(text=label("🔴 Не знаю", "unknown"), callback_data="difficulty_unknown"),
            ],
            [InlineKeyboardButton(text="📖 Развернутый ответ", callback_data="show_detail_answer")],
            [InlineKeyboardButton(text="💡 Примеры использования", callback_data="show_examples_answer")],
            [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_answer")],
            [
                InlineKeyboardButton(text="↩️ Назад в раздел", callback_data="back_to_random_section"),
                InlineKeyboardButton(text="🏠 На главную", callback_data="back_main")
            ],
        ]
    )

def updated_keyboard(mark):
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=("✅ " if mark == FeedbackMark.KNOW else "") + "🟢 Знаю",
                        callback_data="difficulty_know",
                    ),
                    InlineKeyboardButton(
                        text=("✅ " if mark == FeedbackMark.HARD else "") + "🟡 Сложно",
                        callback_data="difficulty_hard",
                    ),
                    InlineKeyboardButton(
                        text=("✅ " if mark == FeedbackMark.UNKNOWN else "") + "🔴 Не знаю",
                        callback_data="difficulty_unknown",
                    ),
                ],
                [InlineKeyboardButton(text="👁 Показать ответ", callback_data="show_response")],
                [InlineKeyboardButton(text="🎯 Следующий вопрос", callback_data="get_random_question")],
                [
                    InlineKeyboardButton(text="↩️ Назад в раздел", callback_data="back_to_random_section"),
                    InlineKeyboardButton(text="🏠 На главную", callback_data="back_main")
                ],
            ]
        )
