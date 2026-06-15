# app/domains/orders/repository.py

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from domains.base.repository import BaseRepository

from .models import Order, OrderItem


class OrderRepository(
    BaseRepository[Order],
):
    model = Order

    async def get_order_by_id(
        self,
        session: AsyncSession,
        order_id: int,
    ) -> Order | None:

        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                selectinload(Order.items),
            )
        )

        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_all_orders(
        self,
        session: AsyncSession,
    ) -> list[Order]:

        stmt = (
            select(Order)
            .options(
                selectinload(Order.items),
            )
            .order_by(Order.id.desc())
        )

        result = await session.execute(stmt)

        return list(result.scalars().all())

    async def get_user_orders(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> list[Order]:

        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(
                selectinload(Order.items),
            )
            .order_by(Order.id.desc())
        )

        result = await session.execute(stmt)

        return list(result.scalars().all())

    async def create_order_item(
        self,
        session: AsyncSession,
        **kwargs,
    ) -> OrderItem:

        item = OrderItem(**kwargs)

        session.add(item)

        await session.flush()

        return item

    async def add_order_item(
            self,
            session: AsyncSession,
            **kwargs,
    ) -> OrderItem:
        item = OrderItem(**kwargs)

        session.add(item)
        await session.flush()

        return item

    async def delete_order_item(
            self,
            session: AsyncSession,
            item: OrderItem,
    ) -> None:
        await session.delete(item)
        await session.flush()

    async def get_order_item_by_id(
            self,
            session: AsyncSession,
            order_id: int,
            item_id: int,
    ) -> OrderItem | None:
        stmt = select(OrderItem).where(
            OrderItem.id == item_id,
            OrderItem.order_id == order_id,
        )

        result = await session.execute(stmt)
        return result.scalar_one_or_none()