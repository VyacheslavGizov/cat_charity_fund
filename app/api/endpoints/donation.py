from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate, DonationForAdminDB, DonationForUserDB,)


router = APIRouter()


@router.post(
    '/',
    response_model=DonationForUserDB,
    response_model_exclude_none=True,
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Сделать пожертвование."""

    donation = await donation_crud.create(donation, session)
    return donation


@router.get(
    '/',
    response_model=list[DonationForAdminDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех пожертвований."""

    donations = await donation_crud.get_all(session)
    return donations


@router.get(
    '/my',
    response_model=list[DonationForUserDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        # user
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""

    # Здесь будет метод, фильтующий по пользователю
    donations = await donation_crud.get_all(session)
    return donations
