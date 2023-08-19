from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, KeyboardButton)

from bot.commands.functions import show_unsub_text
from bot.commands.stateform import StateForm
from bot.db import User


async def start_command(message: types.Message, state: FSMContext):
    if User.is_sub_user:
        keyboard_markup = ReplyKeyboardBuilder()
        keyboard_markup.row(
            KeyboardButton(
                text='Рецепт из имеющегося'
            )
        )
        await message.answer(
            'Выберите кнопку',
            reply_markup=keyboard_markup.as_markup(resize_keyboard=True)
        )
        await state.set_state(StateForm.GET_BUTTON)
    else:
        await show_unsub_text(
            message=message
        )
