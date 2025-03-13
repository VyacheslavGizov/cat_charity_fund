from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def create(
            self,
            scheme_object,
            session: AsyncSession,
    ):
        db_object = self.model(**scheme_object.dict())
        session.add(db_object)
        await session.commit()  # Здесь нужно ловить исключение и делать rollback
        await session.refresh(db_object)
        return db_object
