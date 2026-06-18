from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from domains.orders.models import OrderStatus
from domains.orders.service import OrderService

from .exceptions import (
    PaymentNotFoundException,
)
from .models import (
    Payment,
    PaymentStatus,
)
from .provider import FakePaymentProvider
from .repository import PaymentRepository


class PaymentService:

    def __init__(self):
        self.repository = PaymentRepository()
        self.order_service = OrderService()
        self.provider = FakePaymentProvider()

    async def create_payment(
        self,
        session: AsyncSession,
        order_id: int,
    ) -> tuple[Payment, str]:

        order = await self.order_service.get_order(
            session=session,
            order_id=order_id,
        )

        total_amount = Decimal("0")

        for item in order.items:
            total_amount += item.price * item.quantity

        provider_payment = await self.provider.create_payment(
            amount=float(total_amount),
            order_id=order.id,
        )

        payment = await self.repository.create(
            session=session,
            order_id=order.id,
            provider="fake",
            provider_payment_id=provider_payment["id"],
            amount=total_amount,
            status=PaymentStatus.PENDING,
        )

        await session.commit()

        return (
            payment,
            provider_payment["confirmation_url"],
        )

    async def get_payment(
        self,
        session: AsyncSession,
        payment_id: int,
    ) -> Payment:

        payment = await self.repository.get_by_id(
            session=session,
            obj_id=payment_id,
        )

        if payment is None:
            raise PaymentNotFoundException()

        return payment

    async def mark_succeeded(
        self,
        session: AsyncSession,
        payment_id: int,
    ) -> Payment:

        payment = await self.get_payment(
            session=session,
            payment_id=payment_id,
        )

        payment.status = PaymentStatus.SUCCEEDED

        order = payment.order
        order.status = OrderStatus.PAID

        await session.commit()

        return payment