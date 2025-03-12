from sqlalchemy import Column, Text

from app.core.db import InvestInfoAndDatesAbstractModel
# может все модели в один файл или все импорты сразу в пакет


class Donation(InvestInfoAndDatesAbstractModel):
    # user_id
    comment = Column(Text)
