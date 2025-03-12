from sqlalchemy import Column, Text

from .abstracts import InvestInfoAndDatesAbstractModel


class Donation(InvestInfoAndDatesAbstractModel):
    # user_id
    comment = Column(Text)
