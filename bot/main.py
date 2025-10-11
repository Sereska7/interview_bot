import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot.internal.handlers.start import router as router_start
from bot.pkg.models.core.containers import ContainerMiddleware
from bot.pkg.settings import settings
from bot.configuration import __containers__


async def main():
    load_dotenv()

    bot = Bot(token=settings.BotSettings.BOT_TOKEN)
    dp = Dispatcher()

    # Роутеры
    dp.include_router(router_start)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    try:
        print("Bot online")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot offline")
