import asyncio
import logging
import os

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from sqlalchemy import URL

from bot.commands.bot_commands import bot_commands
from commands import register_user_commands
from bot.db import create_async_engine, proceed_schemas, BaseModel


async def main() -> None:
    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    logging.basicConfig(level=logging.DEBUG)
    token = os.getenv("TELEGRAM_API_KITCHEN")

    dispatcher = Dispatcher()
    bot = Bot(token=token)
    await bot.set_my_commands(commands=commands_for_bot)

    register_user_commands(router=dispatcher)

    postgres_url = URL.create(
        "postgresql+asyncpg",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host="127.0.0.1",
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
    )
    async_engine = create_async_engine(postgres_url)
    await proceed_schemas(async_engine, BaseModel.metadata)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot has been stopped")
