"""VPN Bot — single bot, data-driven, admin + user panels."""

from __future__ import annotations

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand

from bot.config import config
from bot.database import engine
from bot.database.base import Base
from bot.middlewares import DatabaseMiddleware, AuthMiddleware
from bot.handlers.admin import router as admin_router
from bot.handlers.user import router as user_router
from bot.scheduler import start_scheduler, stop_scheduler

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created.")

    await bot.set_my_commands([
        BotCommand(command="start", description="🚀 Запустить бота"),
        BotCommand(command="help", description="❓ Помощь / VPN"),
    ])
    logger.info("Bot commands set.")

    start_scheduler()


async def on_shutdown() -> None:
    stop_scheduler()
    await engine.dispose()
    logger.info("Shutdown complete.")


async def main() -> None:
    logging.basicConfig(
        level=getattr(logging, config.log_level, logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        stream=sys.stdout,
    )

    bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    dp.message.outer_middleware(DatabaseMiddleware())
    dp.callback_query.outer_middleware(DatabaseMiddleware())
    dp.message.outer_middleware(AuthMiddleware())
    dp.callback_query.outer_middleware(AuthMiddleware())

    dp.include_routers(admin_router, user_router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    logger.info("VPN Bot started!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
