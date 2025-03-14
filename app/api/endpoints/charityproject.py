from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.charityproject import (
    CharityProjecDB,
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.core.db import get_async_session
from app.crud.charityproject import charity_project_crud
from app.api.validators import check_project_name_duplicate


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjecDB,
    response_model_exclude_none=True,
)
async def create_charity_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создаёт благотварительный проект."""

    await check_project_name_duplicate(project.name, session)
    project = await charity_project_crud.create(project, session)
    return project


@router.get(
    '/',
    response_model=list[CharityProjecDB],
    response_model_exclude_none=True,
)
async def get_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список всех проектов."""

    all_projects = await charity_project_crud.get_all(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjecDB,
    response_model_exclude_none=True
)
async def update_project(
    project_id: int,
    project_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await charity_project_crud.get(project_id, session)  # Проверить, что такой объект существует
    project = await charity_project_crud.update(project, project_data, session)
    return project