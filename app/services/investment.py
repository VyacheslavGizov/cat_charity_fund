from datetime import datetime


def donations_distribution(target, sources):
    changeds = []
    for source in sources:
        target_remainder = target.full_amount - target.invested_amount
        source_remainder = source.full_amount - source.invested_amount
        invested_amount = (
            source_remainder if target_remainder > source_remainder
            else target_remainder)
        for item in [target, source]:
            item.invested_amount += invested_amount
            if item.invested_amount == item.full_amount:
                item.fully_invested = True
                item.close_date = datetime.now()
        changeds.append(source)
        if target.fully_invested:
            break
    changeds.append(target)
    return changeds
