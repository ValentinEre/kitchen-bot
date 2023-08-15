from sqlalchemy import Column, VARCHAR, INTEGER

from .base import BaseModel


class Recept(BaseModel):
    __tablename__ = "Receipts"

    # id recept
    recept_id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    # name of recept
    recept_name = Column(VARCHAR(64), unique=False, nullable=False)
    preparation = Column(VARCHAR, unique=False, nullable=False)

    def __str__(self) -> str:
        return f"<User:{self.recept_id}>"
