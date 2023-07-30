from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, CallbackQuery

from bot.db.user import is_sub_user


class SubscribeCheck(BaseMiddleware):
    subscribe_result: bool

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        bot: Bot = data['bot']
        user_id = event.from_user.id

        if await is_sub_user(bot=bot, user_id=user_id):
            self.subscribe_result = True
        else:
            self.subscribe_result = False
