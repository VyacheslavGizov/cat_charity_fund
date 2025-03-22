from datetime import datetime
from typing import TypeVar

from app.models.abstracts import InvestInfoAndDatesAbstractModel


ModelType = TypeVar('ModelType', bound=InvestInfoAndDatesAbstractModel)


def donations_distribution(
        target: ModelType,
        sources: list[ModelType]
) -> list[ModelType]:
    changeds = [target]
    for source in sources:
        changeds.append(source)
        target_remainder = get_remainder(target)
        source_remainder = get_remainder(source)
        if target_remainder < source_remainder:
            investment(target, source, amount=target_remainder)
            close_investment_object(target)
            break
        investment(target, source, amount=source_remainder)
        close_investment_object(source)
        if target_remainder > source_remainder:
            continue
        close_investment_object(target)
        break
    return changeds


def get_remainder(object: ModelType):
    return object.full_amount - object.invested_amount


def investment(target: ModelType, source: ModelType, amount: int):
    target.invested_amount += amount
    source.invested_amount += amount


def close_investment_object(object: ModelType):
    object.fully_invested = True
    object.close_date = datetime.now()
