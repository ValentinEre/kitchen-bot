from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, CallbackQuery

from bot.db.user import is_sub_user, User


class SubscribeCheck(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        bot: Bot = data['bot']
        user_id = event.from_user.id
        if await is_sub_user(bot=bot, user_id=user_id):
            User.is_sub_user = True
        else:
            User.is_sub_user = False

        return await handler(event, data)
