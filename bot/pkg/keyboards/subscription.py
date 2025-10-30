from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

subscription_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оформить подписку", callback_data="buy_subscription")],
    ]
)