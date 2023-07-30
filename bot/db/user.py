import datetime

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember
from sqlalchemy import Column, VARCHAR, DATE, select, BIGINT
from sqlalchemy.orm import sessionmaker

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "Users"

    # id from telegram
    user_id = Column(BIGINT, primary_key=True, unique=True, nullable=False)
    # username from telegram
    user_name = Column(VARCHAR(32), unique=False, nullable=True)
    # first reg date
    user_date = Column(DATE, default=datetime.date.today())
    # last visit
    user_last_date = Column(DATE, onupdate=datetime.date.today())


async def is_user_exists(user_id: int, session_maker: sessionmaker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(
                select(User).where(User.user_id == user_id)
            )
            result = sql_res.first()
            return bool(result)


async def create_user(
        user_id: int,
        username: str,
        session_maker: sessionmaker
) -> None:
    async with session_maker() as session:
        async with session.begin():
            user = User(
                user_id=user_id,
                user_name=username,
            )
            session.add(user)


async def is_sub_user(bot: Bot, user_id):
    chat_id = '-1001915744049'

    chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    if chat_member == ChatMemberOwner or ChatMemberMember or ChatMemberAdministrator:
        return True
    return False
