__all__ = ['register_user_commands', 'bot_commands']

from aiogram import Router
from aiogram.filters import Command, CommandStart

from bot.commands.help import help_command
from bot.commands.start import start_command


def register_user_commands(router: Router) -> None:
    router.message.register(start_command, CommandStart())
    router.message.register(help_command, Command(commands=['help']))
