__all__ = ['register_user_commands', 'bot_commands', 'StateForm', 'SubscribeCheck']

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from bot.commands.stateform import StateForm
from bot.commands.help import help_command
from bot.commands.recepts import  recept_with_param, users_product
from bot.commands.start import start_command
from bot.middleware.subscribe_check import SubscribeCheck


def register_user_commands(router: Router) -> None:
    router.message.register(start_command, CommandStart())
    router.message.register(help_command, Command(commands=['help']))
    router.message.register(recept_with_param, F.text == 'Рецепт из имеющегося', StateForm.GET_BUTTON)
    router.message.register(users_product, StateForm.GET_PRODUCT)
