from aiogram import types
from aiogram.utils.keyboard import (ReplyKeyboardMarkup, ReplyKeyboardBuilder, InlineKeyboardMarkup,
                                    InlineKeyboardBuilder, KeyboardButton, InlineKeyboardButton)


async def start_command(message: types.Message):
    menu_builder = ReplyKeyboardBuilder()

    menu_builder.row(
        KeyboardButton(
            text='Случайный рецепт'
        ),
        KeyboardButton(
            text='Рецепт из имеющегося'
        )
    )
    menu_builder.row(
        KeyboardButton(
            text='789'
        )
    )

    await message.answer(
        'Menu',
        reply_markup=menu_builder.as_markup(resize_keyboard=True)
    )
