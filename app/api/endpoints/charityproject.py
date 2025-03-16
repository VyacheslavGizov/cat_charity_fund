from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.charityproject import (
    CharityProjecDB,
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.core.db import get_async_session
from app.crud.charityproject import charity_project_crud
from app.api.validators import check_project_name_duplicate


PROJECT_IS_CLOSED = ('Проект \'{project_name}\' закрыт, '
                     'редактирование недоступно!')
WRONG_FULL_AMOUNT = ('Нельзя установить значение full_amount меньше уже '
                     'вложенной суммы: {invested}.')

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
    """
    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    # Может все валидации перенести в отдельный модуль?
    # Проект существует
    project = await charity_project_crud.get_or_404(project_id, session)
    # Проект не закрыт
    if project.fully_invested:
        raise HTTPException(
            400,  # Точно ли такой код
            detail=PROJECT_IS_CLOSED.format(project_name=str(project))
        )
    # Требуемая сумма не меньше вложенной
    update_data = project_data.dict(exclude_unset=True)
    new_full_amount = update_data.get('full_amount', None)
    invested_ammount = project.invested_amount
    if new_full_amount and new_full_amount < invested_ammount:
        raise HTTPException(
            400,
            detail=WRONG_FULL_AMOUNT.format(invested=invested_ammount)
        )
    project = await charity_project_crud.update(project, update_data, session)
    return project
