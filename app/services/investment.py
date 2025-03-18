from typing import Union

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


UNSUCCESFUL_INVESTMENT = (
    'Возникла ошибка при распределении средств по проектам.')


ProjectOrDonationType = Union[CharityProject, Donation]


async def donations_distribution(
        distributed: ProjectOrDonationType,
        destinations: list[ProjectOrDonationType],
        session: AsyncSession
) -> ProjectOrDonationType:
    if not destinations:
        return distributed
    processed_items = [distributed]
    for destination in destinations:
        processed_items.append(destination)
        temp_distributed_remainder = distributed.remainder
        temp_destination_remainder = destination.remainder
        if temp_distributed_remainder < temp_destination_remainder:
            destination.invested_amount += temp_distributed_remainder
            distributed.close()
            break
        destination.close()
        if temp_distributed_remainder > temp_destination_remainder:
            distributed.invested_amount += temp_destination_remainder
            continue
        distributed.close()
        break
    try:
        session.add_all(processed_items)
        await session.commit()
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNSUCCESFUL_INVESTMENT
        )
    await session.refresh(distributed)
    return distributed
