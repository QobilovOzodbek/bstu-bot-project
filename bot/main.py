import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from app.db.database import init_db

from bot.handlers.start import router as start_router
from bot.handlers.menu import router as menu_router
from bot.handlers.news import router as news_router
from bot.handlers.links import router as links_router
from bot.handlers.announcements import router as announcements_router
from bot.handlers.leadership import router as leadership_router
from bot.handlers.contact import router as contact_router
from bot.handlers.appeals import router as appeals_router
from bot.handlers.questions import router as questions_router
from bot.handlers.admin import router as admin_router

load_dotenv()


async def main():
    init_db()

    bot_token = getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError("BOT_TOKEN topilmadi. .env faylni tekshiring.")

    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(news_router)
    dp.include_router(announcements_router)
    dp.include_router(leadership_router)
    dp.include_router(contact_router)
    dp.include_router(links_router)
    dp.include_router(appeals_router)
    dp.include_router(questions_router)
    dp.include_router(admin_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())