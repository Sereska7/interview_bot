from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def level_keyboard(topic: str) -> InlineKeyboardMarkup:
    """
    Возвращает inline-клавиатуру выбора уровня для конкретной темы.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🧩 Junior", callback_data=f"level:{topic}:junior"),
                InlineKeyboardButton(text="⚙️ Middle", callback_data=f"level:{topic}:middle"),
                InlineKeyboardButton(text="🧠 Senior", callback_data=f"level:{topic}:senior")
            ],
            [
                InlineKeyboardButton(text="↩️ Назад", callback_data=f"level:{topic}:back")
            ]
        ]
    )