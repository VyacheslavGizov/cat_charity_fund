from sqlalchemy import Column, Text, ForeignKey, Integer

from .abstracts import InvestInfoAndDatesAbstractModel


class Donation(InvestInfoAndDatesAbstractModel):
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user')
    )
    comment = Column(Text)
