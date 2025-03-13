from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.core.config import (
    MAX_NAME_LENGTH,
    MIN_DESCRIPTION_LENGTH,
    MIN_NAME_LENGTH,
)


# Возможжно будет что-то общее для двух схем
class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None, min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    description: Optional[str] = Field(None, min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: Optional[PositiveInt]

    class Config:  # Запрет на передачу в схему неописанных полей
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ..., min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    description: str = Field(..., min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass
    #  Может валидатор на то, что name not is None


class CharityProjecDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
