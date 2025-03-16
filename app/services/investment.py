from sqlalchemy.ext.asyncio import AsyncSession


async def investment(distributed, destinations, session: AsyncSession):
    processed_items = [distributed]
    for destination in destinations:
        processed_items.append(destination)
        temp_distributed_remainder = distributed.remainder
        temp_destination_remainder = destination.remainder
        if temp_distributed_remainder < temp_destination_remainder:
            destination.invested_amount += temp_distributed_remainder
            distributed.close()
            break
        destination.close()
        if temp_distributed_remainder > temp_destination_remainder:
            distributed.invested_amount += temp_destination_remainder
            continue
        distributed.close()
        break
    session.add_all(processed_items)
    await session.commit()  # Здесь делать rollback
    await session.refresh(distributed)
    return distributed
