from decimal import (
    Decimal,
    ROUND_HALF_UP,
)

from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings


from domains.orders.models import OrderStatus
from domains.orders.service import OrderService

from .exceptions import PaymentNotFoundException
from .models import (
    Payment,
    PaymentStatus,
)
from .provider import FakePaymentProvider,YookassaPaymentProvider
from .repository import PaymentRepository


class PaymentService:

    def __init__(self):
        self.repository = PaymentRepository()
        self.order_service = OrderService()
        self.provider = YookassaPaymentProvider(
    shop_id=settings.yookassa.shop_id,
    secret_key=settings.yookassa.secret_key,
)
        #self.provider= FakePaymentProvider()

    # -------------------------
    # CREATE PAYMENT
    # -------------------------
    async def create_payment(
        self,
        session: AsyncSession,
        order_id: int,
    ) -> tuple[Payment, str]:

        order = await self.order_service.get_order(
            session=session,
            order_id=order_id,
        )

        total_amount = Decimal("0.00")

        for item in order.items:
            total_amount += item.price * item.quantity

        total_amount = total_amount.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        provider_payment = await self.provider.create_payment(
            amount=total_amount,
            order_id=order.id,
        )

        payment = await self.repository.create(
            session=session,
            order_id=order.id,
            provider="yookassa",
            #provider="fake",
            provider_payment_id=provider_payment["id"],
            amount=total_amount,
            status=PaymentStatus.PENDING,
        )

        await session.commit()

        return payment, provider_payment["confirmation_url"]

    # -------------------------
    # GET PAYMENT
    # -------------------------
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

    # -------------------------
    # PUBLIC: mark by payment id
    # -------------------------
    async def mark_succeeded(
        self,
        session: AsyncSession,
        payment_id: int,
    ) -> Payment:

        payment = await self.get_payment(
            session=session,
            payment_id=payment_id,
        )

        return await self._mark_succeeded(session, payment)

    # -------------------------
    # PUBLIC: mark by provider id (WEBHOOK USE)
    # -------------------------
    async def mark_succeeded_by_provider_id(
        self,
        session: AsyncSession,
        provider_payment_id: str,
    ) -> Payment:

        payment = await self.repository.get_by_provider_payment_id(
            session=session,
            provider_payment_id=provider_payment_id,
        )

        if payment is None:
            raise PaymentNotFoundException()

        return await self._mark_succeeded(session, payment)

    # -------------------------
    # PRIVATE CORE LOGIC
    # -------------------------
    async def _mark_succeeded(
        self,
        session: AsyncSession,
        payment: Payment,
    ) -> Payment:

        # идемпотентность (важно для webhook)
        if payment.status == PaymentStatus.SUCCEEDED:
            return payment

        payment.status = PaymentStatus.SUCCEEDED

        order = payment.order
        order.status = OrderStatus.PAID

        await session.commit()

        return payment