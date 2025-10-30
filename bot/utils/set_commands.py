from aiogram import Bot
from aiogram import Bot
from aiogram.types import BotCommand

async def set_my_commands(bot: Bot):
    """
    Регистрирует список команд бота в Telegram.
    Вызывается один раз при старте приложения.
    """
    commands = [
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="menu", description="Главное меню"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="progress", description="Ваш прогресс"),
        BotCommand(command="about", description="О боте"),
        BotCommand(command="feedback", description="Обратная связь"),
        BotCommand(command="subscription", description="Оформить или продлить подписку"),
    ]

    # 👇 вот эта строка обязательна — она сообщает Telegram о командах
    await bot.set_my_commands(commands)
