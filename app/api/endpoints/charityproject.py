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
from app.crud.donation import donation_crud
from app.api.validators import check_project_name_duplicate
from app.services.investment import donations_distribution
from app.core.user import current_superuser


PROJECT_IS_CLOSED = ('{project} - проект закрыт, редактирование '
                     'недоступно!')
WRONG_FULL_AMOUNT = ('Нельзя установить значение full_amount меньше уже '
                     'вложенной суммы: {invested}.')
PROJECT_IS_INVESTED_ERROR = ('{project} - были внесены средства, '
                             'не подлежит удалению!')

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjecDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создаёт благотварительный проект."""

    await check_project_name_duplicate(project.name, session)
    project = await charity_project_crud.create(project, session)
    project = await donations_distribution(
        distributed=project,
        destinations=await donation_crud.get_opens(session),
        session=session
    )
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
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
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
    project = await charity_project_crud.get_or_404(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            400,  # Точно ли такой код
            detail=PROJECT_IS_CLOSED.format(project=project)
        )
    update_data = project_data.dict(exclude_unset=True)
    new_full_amount = update_data.get('full_amount', None)
    new_name = update_data.get('name', None)
    if new_name is not None:
        await check_project_name_duplicate(new_name, session)
    if new_full_amount is None:
        project = await charity_project_crud.update(
            project, update_data, session)
        return project
    invested_ammount = project.invested_amount
    if new_full_amount < invested_ammount:
        raise HTTPException(
            400,
            detail=WRONG_FULL_AMOUNT.format(invested=invested_ammount)
        )
    if new_full_amount == invested_ammount:
        project.close()
    project = await charity_project_crud.update(project, update_data, session)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjecDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы
    средства, его можно только закрыть.
    """

    project = await charity_project_crud.get_or_404(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            400,
            detail=PROJECT_IS_INVESTED_ERROR.format(
                project=project)
        )
    project = await charity_project_crud.delete(project, session)
    return project
