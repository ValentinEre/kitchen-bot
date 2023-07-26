from aiogram import types
from aiogram.filters import CommandObject

from bot.commands import bot_commands


async def help_command(message: types.Message, command: CommandObject):
    if command.args:
        for cmd in bot_commands:
            if cmd[0] == command.args:
                return await message.answer(
                    f'{cmd[0]} - {cmd[2]}'
                )
        else:
            return await message.answer('Command not found')
    return await message.answer(
        'Help with the bot'
    )
