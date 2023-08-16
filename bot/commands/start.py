from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, KeyboardButton, InlineKeyboardBuilder)

from bot.commands.stateform import StateForm
from bot.db import User


async def start_command(message: types.Message, state: FSMContext):
    chat_link = 'https://t.me/+lar9adBYtUg0N2Zi'
    chat_name = 'Кулинарная Академия: Рецепты и Лайфхаки'
    message_for_unsub_user = 'Чтобы пользаваться этим замечательным ботом, пожалуйста подпишитесь на канал'
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
        keyboard_markup = InlineKeyboardBuilder()
        keyboard_markup.button(
            text=chat_name,
            url=chat_link
        )
        await message.answer(
            message_for_unsub_user,
            reply_markup=keyboard_markup.as_markup(resize_keyboard=True)
        )
