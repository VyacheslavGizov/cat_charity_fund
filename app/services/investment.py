from typing import Union

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


ProjectOrDonationType = Union[CharityProject, Donation]


def investment(target, sources):  # Аннотации потом
    changeds = [target]
    if not sources:
        return changeds
    for source in sources:
        changeds.append(source)
        target_remainder = target.remainder
        source_remainder = source.remainder
        if target_remainder < source_remainder:
            source.invested_amount += target_remainder
            target.close()
            break
        source.close()
        if target_remainder > source_remainder:
            target.invested_amount += source_remainder
            continue
        target.close()
        break
    return changeds
