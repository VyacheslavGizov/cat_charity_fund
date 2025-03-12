from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declared_attr, declarative_base, sessionmaker

from app.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


# Возможно перенести остюда в пакет/файл с моделями
class InvestInfoAndDatesAbstractModel(Base):
    __abstract__ = True

    full_amount = Column(Integer, default=0)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, index=True, default=datetime.now)
    close_date = Column(DateTime)


engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
