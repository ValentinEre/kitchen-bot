from aiogram import types
from aiogram.filters import CommandObject
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bot.commands import bot_commands, StateForm
from bot.db import User


async def help_command(message: types.Message, command: CommandObject):
    chat_link = 'https://t.me/+lar9adBYtUg0N2Zi'
    chat_name = 'Кулинарная Академия: Рецепты и Лайфхаки'
    message_for_unsub_user = 'Чтобы пользаваться этим замечательным ботом, пожалуйста подпишитесь на канал'
    if User.is_sub_user:
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
    else:
        keyboard_markup = InlineKeyboardBuilder()
        keyboard_markup.button(
            text=chat_name,
            url=chat_link
        )
        await message.answer(
            message_for_unsub_user,
            reply_markup=keyboard_markup.as_markup(resize_keyboard=True)
        )
