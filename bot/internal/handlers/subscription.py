from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.pkg.keyboards.subscription import subscription_kb
from bot.utils import delete_old_messages, save_message_id

router = Router()


@router.message(F.text == "💎 Подписка")
async def show_subscription(
    message: types.Message,
    state: FSMContext,
):
    await delete_old_messages(message.bot, message.chat.id, state)
    await message.delete()

    msg = await message.answer(
        "💎 <b>Подписка PRO</b>\n\n"
        "Раскрой весь потенциал бота:\n"
        "✅ Полный доступ ко всем темам и уровням\n"
        "📊 Расширенная статистика и аналитика\n"
        "🔁 Повторение ошибок и умное обучение\n"
        "🧩 Новые тесты и обновления первыми\n\n"
        "💰 <b>Цена:</b> 299 ₽ / 30 дней\n\n",
        parse_mode="HTML",
        reply_markup=subscription_kb
    )

    await save_message_id(state, msg.message_id)


@router.message(Command("subscription"))
async def cmd_subscription(message: types.Message, state: FSMContext):
    """Показывает экран подписки (как при нажатии кнопки 💎 Подписка)."""
    await show_subscription(message, state)


# 💳 Нажатие на кнопку “Оформить подписку”
@router.callback_query(F.data == "buy_subscription")
async def process_buy_subscription(callback: types.CallbackQuery):
    prices = [types.LabeledPrice(label="Подписка PRO (30 дней)", amount=29900)]  # 299 ₽

    await callback.message.answer_invoice(
        title="Подписка PRO",
        description="Доступ ко всем темам, аналитике и обновлениям.",
        provider_token="381764678:LIVE:abcdef123",  # заменишь на свой токен ЮKassa
        currency="RUB",
        prices=prices,
        payload="subscription_pro"
    )
    await callback.answer()
