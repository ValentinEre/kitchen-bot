from sqlalchemy import Column, INTEGER

from .base import BaseModel


class Intermediate(BaseModel):
    __tablename__ = "Intermediate"

    # id recept
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    recept_id = Column(INTEGER, unique=False, nullable=False)
    ingredient_id = Column(INTEGER, unique=False, nullable=False)
    unit_id = Column(INTEGER, unique=False, nullable=False)

    def __str__(self) -> str:
        return f"<User:{self.recept_id}>"
