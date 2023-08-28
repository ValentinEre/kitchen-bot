from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import (InlineKeyboardBuilder)

from bot.commands.functions import show_subscription_text
from bot.commands.stateform import StateForm
from bot.db import User


async def start_command(message: types.Message, state: FSMContext):
    if User.is_sub_user:
        keyboard_markup = InlineKeyboardBuilder()
        keyboard_markup.button(
            text='Рецепт из имеющегося',
            callback_data='Рецепт из имеющегося'
        )

        await message.answer(
            'Нажмите кнопку',
            reply_markup=keyboard_markup.as_markup(resize_keyboard=True)
        )
        await state.set_state(StateForm.GET_BUTTON)
    else:
        await show_subscription_text(
            message=message
        )
