from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.charityproject import (
    CharityProjectCreate,
    CharityProjecDB,
)
from app.core.db import get_async_session
from app.crud.charityproject import charity_project_crud


router = APIRouter()


@router.post(
    '/charity_project/',
    response_model=CharityProjecDB
)
async def create_charity_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    #  Проверить, что переданное название проекта уникально
    project = await charity_project_crud.create(project, session)
    return project
