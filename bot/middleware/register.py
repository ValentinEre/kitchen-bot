from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.orm import sessionmaker

from bot.db.user import is_user_exists, create_user


class RegisterCheck(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id

        session_maker: sessionmaker = data['session_maker']
        redis = data['redis']

        if not await is_user_exists(user_id=user_id, session_maker=session_maker, redis=redis):
            await create_user(
                user_id=event.from_user.id,
                username=event.from_user.first_name,
                session_maker=session_maker
            )

        return await handler(event, data)
