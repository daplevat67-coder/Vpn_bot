"""Simple VPN bot — /start and /help only."""

from __future__ import annotations

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from aiogram.filters import CommandStart, Command

logger = logging.getLogger(__name__)

BOT_TOKEN = "8535678185:AAGvdo83C7VUpDDG-suDDcV_nzhlGTS0ULs"

HELP_TEXT = (
    "Здравствуйте!\n\n"
    "Чтобы подключить VPN:\n\n"
    "1️⃣ AmneziaVPN\n"
    "Скачайте AmneziaVPN для Android или\n"
    "Скачайте Defolt VPN для iPhone\n\n"
    "2️⃣ happ / v2raytun / foxray\n"
    "Скачайте приложение happ, v2raytun или foxray\n\n"
    "Если у вас другая проблема:"
)

TICKET_KB = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📩 Открыть тикет", url="https://t.me/TimeTag_Tim_bot?start=ticket")],
])


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    await bot.set_my_commands([
        BotCommand(command="start", description="🚀 Запустить бота"),
        BotCommand(command="help", description="❓ Помощь / VPN"),
    ])

    @dp.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        await message.answer(
            "👋 Добро пожаловать!\n\n"
            "Нажмите /help чтобы узнать как подключить VPN."
        )

    @dp.message(Command("help"))
    async def cmd_help(message: Message) -> None:
        await message.answer(HELP_TEXT, reply_markup=TICKET_KB)

    logger.info("Bot started!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
