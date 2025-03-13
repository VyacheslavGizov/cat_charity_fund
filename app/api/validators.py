from http import HTTPStatus

from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud


NONUNIQUE_PROJECT_NAME = 'Проект с именем \'{name}\' уже существует.'


async def check_project_name_duplicate(
        name: str,
        session: AsyncSession
) -> None:
    project_id = await charity_project_crud.get_id_by_name(name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=NONUNIQUE_PROJECT_NAME.format(name=name)
        )
