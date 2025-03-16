from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, DateTime

from app.core.db import Base


class InvestInfoAndDatesAbstractModel(Base):
    __abstract__ = True

    full_amount = Column(Integer, default=0)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, index=True, default=datetime.now)
    close_date = Column(DateTime)

    @property
    def remainder(self):
        return self.full_amount - self.invested_amount

    def close(self):
        self.invested_amount = self.full_amount
        self.fully_invested = True
        self.close_date = datetime.now()
