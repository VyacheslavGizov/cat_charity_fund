from sqlalchemy import Column, String, Text

from .abstracts import InvestInfoAndDatesAbstractModel
from app.core.config import MAX_NAME_LENGTH


class CharityProject(InvestInfoAndDatesAbstractModel):
    name = Column(String(MAX_NAME_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
