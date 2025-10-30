import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot.internal.handlers import routers
from bot.pkg.settings import settings
from bot.configuration import __containers__
from bot.utils.set_commands import set_my_commands


async def main():
    load_dotenv()

    bot = Bot(token=settings.BotSettings.BOT_TOKEN)
    dp = Dispatcher()
    await set_my_commands(bot)

    # Роутеры
    for router in routers:
        dp.include_router(router)

    await dp.start_polling(bot, skip_updates=False)


if __name__ == "__main__":
    try:
        print("Bot online")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot offline")
