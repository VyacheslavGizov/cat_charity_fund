from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charityproject import CharityProject


class CRUDCharityProject(CRUDBase):
    pass


charity_project_crud = CRUDBase(CharityProject)
