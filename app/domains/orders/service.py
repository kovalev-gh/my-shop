# app/domains/orders/service.py

from sqlalchemy.ext.asyncio import AsyncSession

from domains.products.exceptions import ProductNotFoundException
from domains.products.repository import ProductRepository
from domains.mailing.send_order_notification import send_order_notification_email

from .exceptions import (
    OrderNotFoundException,
    NotEnoughStockException,
    OrderItemNotFoundException
)
from .models import Order
from .repository import OrderRepository
from .schemas import OrderCreate


class OrderService:

    def __init__(self):
        self.repository = OrderRepository()
        self.product_repository = ProductRepository()

    async def get_order(
        self,
        session: AsyncSession,
        order_id: int,
    ) -> Order:

        order = await self.repository.get_order_by_id(
            session=session,
            order_id=order_id,
        )

        if order is None:
            raise OrderNotFoundException()

        return order

    async def get_all_orders(
        self,
        session: AsyncSession,
    ) -> list[Order]:

        return await self.repository.get_all_orders(
            session=session,
        )

    async def get_user_orders(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> list[Order]:

        return await self.repository.get_user_orders(
            session=session,
            user_id=user_id,
        )

    async def create_order(
        self,
        session: AsyncSession,
        user_id: int,
        order_in: OrderCreate,
    ) -> Order:

        order = await self.repository.create(
            session=session,
            user_id=user_id,
            promocode=order_in.promocode,
        )

        try:
            for item in order_in.items:

                product = await self.product_repository.get_by_id(
                    session=session,
                    obj_id=item.product_id,
                )

                if product is None:
                    raise ProductNotFoundException()

                if product.stock_quantity < item.quantity:
                    raise NotEnoughStockException(
                        product_id=product.id,
                    )

                await self.repository.create_order_item(
                    session=session,
                    order_id=order.id,
                    product_id=product.id,
                    quantity=item.quantity,
                    price=product.unit_price,
                )

                product.stock_quantity -= item.quantity

            await session.commit()

        except Exception:
            await session.rollback()
            raise

        order = await self.get_order(
            session=session,
            order_id=order.id,
        )

        await send_order_notification_email(order)

        return order

    async def delete_order(
        self,
        session: AsyncSession,
        order_id: int,
    ) -> None:

        order = await self.get_order(
            session=session,
            order_id=order_id,
        )

        await self.repository.delete(
            session=session,
            obj=order,
        )

        await session.commit()

    async def add_item_to_order(
            self,
            session: AsyncSession,
            order_id: int,
            product_id: int,
            quantity: int,
    ) -> Order:

        order = await self.get_order(
            session=session,
            order_id=order_id,
        )

        product = await self.product_repository.get_by_id(
            session=session,
            obj_id=product_id,
        )

        if product is None:
            raise ProductNotFoundException()

        if product.stock_quantity < quantity:
            raise NotEnoughStockException(product_id=product.id)

        existing_item = await self.repository.get_order_item(
            session=session,
            order_id=order_id,
            product_id=product_id,
        )

        if existing_item:
            existing_item.quantity += quantity

        else:
            await self.repository.add_order_item(
                session=session,
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                price=product.unit_price,
            )

        product.stock_quantity -= quantity

        await session.commit()

        return await self.get_order(
            session=session,
            order_id=order.id,
        )

    async def remove_item_from_order(
            self,
            session: AsyncSession,
            order_id: int,
            product_id: int,
            quantity: int | None = None,
    ) -> Order:

        order = await self.get_order(
            session=session,
            order_id=order_id,
        )

        item = await self.repository.get_order_item(
            session=session,
            order_id=order_id,
            product_id=product_id,
        )

        if item is None:
            raise OrderItemNotFoundException()

        product = await self.product_repository.get_by_id(
            session=session,
            obj_id=product_id,
        )

        if product is None:
            raise ProductNotFoundException()

        if quantity is None or quantity >= item.quantity:

            product.stock_quantity += item.quantity

            await self.repository.delete_order_item(
                session=session,
                item=item,
            )

        else:
            item.quantity -= quantity
            product.stock_quantity += quantity

        await session.commit()

        return await self.get_order(
            session=session,
            order_id=order.id,
        )