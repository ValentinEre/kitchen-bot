from sqlalchemy import Column, INTEGER, VARCHAR

from .base import BaseModel


class Ingredient(BaseModel):
    __tablename__ = "Ingredients"

    # id recept
    ingredient_id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    ingredient_name = Column(VARCHAR(64), unique=False, nullable=False)


    def __str__(self) -> str:
        return f"<User:{self.recept_id}>"
