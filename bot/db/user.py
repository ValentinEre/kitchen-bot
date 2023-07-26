import datetime

from sqlalchemy import Column, INTEGER, VARCHAR, DATE

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "Users"

    # id from telegram
    user_id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    # username from telegram
    user_name = Column(VARCHAR(32), unique=False, nullable=True)
    # first reg date
    user_date = Column(DATE, default=datetime.date.today())
    # last visit
    user_last_date = Column(DATE, onupdate=datetime.date.today())

    def __str__(self) -> str:
        return f"<User:{self.user_id}>"
