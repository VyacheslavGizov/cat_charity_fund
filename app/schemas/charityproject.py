from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt

from app.core.config import (
    MAX_NAME_LENGTH,
    MIN_DESCRIPTION_LENGTH,
    MIN_NAME_LENGTH,
)


class CharityProjectBase(BaseModel):  # Возможжно будет что-то общее для двух схем
    id: int
    name: str = Field(
        ..., min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    description: str = Field(..., min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: PositiveInt
    invested_amount: PositiveInt
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]


class CharityProjectCreate(BaseModel):
    name: str = Field(
        ..., min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    description: str = Field(..., min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: PositiveInt


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    description: Optional[str] = Field(None, min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: Optional[PositiveInt]


class CharityProjecDB(BaseModel):
    id: int
    name: str = Field(
        ..., min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)
    description: str = Field(..., min_length=MIN_DESCRIPTION_LENGTH)
    full_amount: PositiveInt
    invested_amount: PositiveInt
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
