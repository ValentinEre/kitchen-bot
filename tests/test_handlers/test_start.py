from unittest.mock import AsyncMock

import pytest as pytest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.commands.start import start_command
from tests.coftest import bot
from tests.utils import TEST_USER, TEST_USER_CHAT


@pytest.mark.asyncio
async def test_start_handler(storage):
    message = AsyncMock()
    keyboard_markup = InlineKeyboardBuilder()
    keyboard_markup.button(
        text='Рецепт из имеющегося',
        callback_data='Рецепт из имеющегося'
    )
    state = FSMContext(
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_USER_CHAT.id)
    )
    await start_command(
        message=message,
        state=state
    )
    assert await state.get_state() is None
    message.answer.assert_called_with('Нажмите кнопку',
                                      reply_markup=keyboard_markup.as_markup(resize_keyboard=True))
