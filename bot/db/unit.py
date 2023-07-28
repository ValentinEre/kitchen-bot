from sqlalchemy import Column, VARCHAR, INTEGER

from .base import BaseModel


class Units(BaseModel):
    __tablename__ = "Units"

    # id recept
    unit_id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    # name of recept
    unit_name = Column(VARCHAR(64), unique=False, nullable=False)

    def __str__(self) -> str:
        return f"<User:{self.recept_id}>"
