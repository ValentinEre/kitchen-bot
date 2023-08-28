from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

chat_link = 'https://t.me/+lar9adBYtUg0N2Zi'
chat_name = 'Кулинарная Академия: Рецепты и Лайфхаки'
message_for_unsub_user = 'Чтобы пользаваться этим замечательным ботом, пожалуйста подпишитесь на канал'


async def show_message(message: types.Message, text: str, inline_keyboard=None):
    await message.answer(
        text=text,
        reply_markup=inline_keyboard
    )


async def show_subscription_text(
        message: types.Message
):
    keyboard_markup = InlineKeyboardBuilder()
    keyboard_markup.button(
        text=chat_name,
        url=chat_link
    )
    await message.answer(
        message_for_unsub_user,
        reply_markup=keyboard_markup.as_markup(resize_keyboard=True)
    )


async def call_show_subscription_text(
        callback: types.CallbackQuery
):
    keyboard_markup = InlineKeyboardBuilder()
    keyboard_markup.button(
        text=chat_name,
        url=chat_link
    )
    await callback.message.edit_text(
        message_for_unsub_user,
        reply_markup=keyboard_markup.as_markup(resize_keyboard=True)
    )
