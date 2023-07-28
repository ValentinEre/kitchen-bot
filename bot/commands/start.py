from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, KeyboardButton)

from bot.commands.stateform import StateForm


async def is_sub_user(bot: Bot, user_id):
    channel = [
        'Кулинарная Академия: Рецепты и Лайфхаки', '-1001915744049', 'https://t.me/+lar9adBYtUg0N2Zi'
    ]

    chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
    if chat_member['status'] == 'member':
        return False
    return True


no_sub_user = 'Для пользования ботом нужно быть подписанным на канал'


async def start_command(message: types.Message, state: FSMContext):
    menu_builder = ReplyKeyboardBuilder()

    menu_builder.row(
        KeyboardButton(
            text='Случайный рецепт'
        ),
        KeyboardButton(
            text='Рецепт из имеющегося'
        )
    )

    await message.answer(
        'Выбери кнопку',
        reply_markup=menu_builder.as_markup(resize_keyboard=True)
    )

    await state.set_state(StateForm.GET_BUTTON)
