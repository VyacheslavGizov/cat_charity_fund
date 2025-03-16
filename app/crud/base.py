from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException


NOT_FOUND_MESSAGE = '\'{object_name}\' c id={object_id} не найден!'


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

    async def get(  # Возможно не нужно
            self,
            object_id: int,
            session: AsyncSession,
    ):
        objects = await session.execute(
            select(self.model).where(self.model.id == object_id))  # Есть более короткий вариант запроса
        return objects.scalars().first()

    async def get_or_404(
            self,
            object_id: int,
            session: AsyncSession
    ):
        object = await self.get(object_id, session)
        if object is None:
            raise HTTPException(
                404,
                detail=NOT_FOUND_MESSAGE.format(
                    object_name=self.model.__name__,
                    object_id=object_id
                )
            )
        return object

    async def get_all(
            self,
            session: AsyncSession,
    ):
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def update(
            self,
            db_object,
            update_data,
            session: AsyncSession,
    ):
        object_data = jsonable_encoder(db_object)  # Может перенести в метод объекта .to_dict()
        for field in update_data:
            if field in object_data:
                setattr(db_object, field, update_data[field])
        session.add(db_object)
        await session.commit()  # Здесь нужно ловить исключение и делать rollback
        await session.refresh(db_object)
        return db_object

    async def delete(
            self,
            db_object,
            session: AsyncSession
    ):
        await session.delete(db_object)
        await session.commit()  # Здесь нужно ловить исключение и делать rollback
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
