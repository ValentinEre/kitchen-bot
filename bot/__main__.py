import asyncio
import os
import pathlib

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from sqlalchemy import URL

from bot.commands import bot_commands
from bot.db import create_async_engine
from bot.db.engine import get_session_maker
from bot.middleware.register import RegisterCheck
from bot.middleware.subscribe_check import SubscribeCheck
from commands import register_user_commands


async def start_bot() -> None:
    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    # logging.basicConfig(level=logging.DEBUG)
    token = os.getenv("TELEGRAM_API_KITCHEN")

    dispatcher = Dispatcher()
    bot = Bot(token=token)
    await bot.set_my_commands(commands=commands_for_bot)

    dispatcher.message.middleware.register(RegisterCheck())
    dispatcher.message.middleware.register(SubscribeCheck())
    register_user_commands(router=dispatcher)

    postgres_url = URL.create(
        "postgresql+asyncpg",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
    )
    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)

    await dispatcher.start_polling(bot, session_maker=session_maker)


def set_env():
    from dotenv import load_dotenv
    path = pathlib.Path(__file__).parent.parent
    dotenv_path = path.joinpath('.env')
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path)


def main():
    try:
        set_env()
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        print("Bot has been stopped")


if __name__ == "__main__":
    main()
