from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def create(
            self,
            object_in,
            session: AsyncSession,  # Нужны ли здесь аннотации?
    ):
        db_object = self.model(**object_in.dict())
        session.add(db_object)
        await session.commit()  # Здесь нужно ловить исключение и делать rollback
        await session.refresh(db_object)
        return db_object

    async def get(
            self,
            object_id: int,
            session: AsyncSession,
    ):
        objects = await session.execute(
            select(self.model).where(self.model.id == object_id))  # Есть более короткий вариант запроса
        return objects.scalars().first()

    async def get_all(
            self,
            session: AsyncSession,
    ):
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def update(
            self,
            db_object,
            object_in,
            session: AsyncSession,
    ):
        object_data = jsonable_encoder(db_object)
        update_data = object_in.dict(exclude_unset=True)
        for field in update_data:
            if field in object_data:
                setattr(db_object, field, update_data[field])
        session.add(db_object)
        await session.commit()  # Здесь нужно ловить исключение и делать rollback
        await session.refresh(db_object)
        return db_object

    # async def get_by_attr(
    #         self,
    #         attr_name: str,
    #         attr_value,
    #         session: AsyncSession,
    # ):
    #     db_objects = await session.execute(
    #         select(self.model).where(
    #             getattr(self.model, attr_name) == attr_value
    #         )
    #     )
    #     return db_objects.scalars().first()
