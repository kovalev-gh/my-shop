import logging
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from domains.orders.models import Order, OrderStatus
from domains.orders.service import OrderService

from .exceptions import (
    PaymentNotFoundException,
    PaymentAlreadyExistsException,
    PaymentAlreadySucceededException,
    PaymentAlreadyCanceledException
)
from .models import Payment, PaymentStatus
from .provider import FakePaymentProvider
from .repository import PaymentRepository


logger = logging.getLogger(__name__)


class PaymentService:

    def __init__(self):
        self.repository = PaymentRepository()
        self.order_service = OrderService()
        self.provider = FakePaymentProvider()

    # -------------------------
    # CREATE PAYMENT
    # -------------------------
    async def create_payment(
        self,
        session: AsyncSession,
        order_id: int,
    ) -> tuple[Payment, str]:

        logger.info("Creating payment for order_id=%s", order_id)

        order = await self.order_service.get_order(
            session=session,
            order_id=order_id,
        )

        logger.info(
            "Order loaded: id=%s items=%s",
            order.id,
            len(order.items),
        )

        # защита от дублей
        existing_payment = await self.repository.get_by_order_id(
            session=session,
            order_id=order.id,
        )
        if existing_payment:
            if existing_payment.status == PaymentStatus.PENDING:
                logger.warning(
                    "Payment already exists for order_id=%s payment_id=%s",
                    order.id,
                    existing_payment.id,
                )
                raise PaymentAlreadyExistsException()

            if existing_payment.status == PaymentStatus.SUCCEEDED:
                logger.warning(
                    "Payment already succeeded for order_id=%s payment_id=%s",
                    order.id, existing_payment.id
                )
                raise PaymentAlreadySucceededException()


            if existing_payment.status == PaymentStatus.CANCELED:
                logger.warning(
                    "Previous payment canceled, creating new one for order_id=%s",
                    order.id,
                )
                #Если статус CANCELED - платеж на этот заказ создать нельзя!
                raise PaymentAlreadyCanceledException()

        # считаем сумму
        total_amount = Decimal("0.00")

        for item in order.items:
            total_amount += item.price * item.quantity

        total_amount = total_amount.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        logger.info(
            "Total amount calculated: order_id=%s amount=%s",
            order.id,
            total_amount,
        )

        provider_payment = await self.provider.create_payment(
            amount=total_amount,
            order_id=order.id,
        )

        logger.info(
            "Provider payment created: provider_id=%s status=%s",
            provider_payment["id"],
            provider_payment["status"],
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

        logger.info(
            "Payment saved: payment_id=%s provider_payment_id=%s",
            payment.id,
            payment.provider_payment_id,
        )

        return payment, provider_payment["confirmation_url"]

    # -------------------------
    # GET PAYMENT
    # -------------------------
    async def get_payment_by_id(
        self,
        session: AsyncSession,
        payment_id: int,
    ) -> Payment:

        logger.info("Fetching payment: payment_id=%s", payment_id)

        payment = await self.repository.get_by_id(
            session=session,
            obj_id=payment_id,
        )

        if payment is None:
            logger.warning("Payment not found: payment_id=%s", payment_id)
            raise PaymentNotFoundException()

        logger.info(
            "Payment found: id=%s status=%s",
            payment.id,
            payment.status,
        )

        return payment

    # -------------------------
    # PUBLIC: mark by payment id
    # -------------------------
    async def mark_succeeded_by_payment_id(
        self,
        session: AsyncSession,
        payment_id: int,
    ) -> Payment:

        logger.info("Mark payment succeeded: payment_id=%s", payment_id)

        payment = await self.get_payment_by_id(
            session=session,
            payment_id=payment_id,
        )

        return await self._mark_succeeded(session, payment)

    # -------------------------
    # PUBLIC: mark by provider id (WEBHOOK ENTRY POINT)
    # -------------------------
    async def mark_succeeded_by_provider_id(
        self,
        session: AsyncSession,
        provider_payment_id: str,
    ) -> Payment:

        logger.info(
            "Webhook received for provider_payment_id=%s",
            provider_payment_id,
        )

        payment = await self.repository.get_by_provider_payment_id(
            session=session,
            provider_payment_id=provider_payment_id,
        )

        if payment is None:
            logger.warning(
                "Payment not found for provider_payment_id=%s",
                provider_payment_id,
            )
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

        logger.info(
            "Marking payment succeeded: payment_id=%s status=%s",
            payment.id,
            payment.status,
        )

        # идемпотентность webhook
        if payment.status == PaymentStatus.SUCCEEDED:
            logger.info(
                "Payment already succeeded: payment_id=%s",
                payment.id,
            )
            return payment

        # обновляем payment
        payment.status = PaymentStatus.SUCCEEDED

        await session.execute(
            update(Order)
            .where(Order.id == payment.order_id)
            .values(status=OrderStatus.PAID)
        )

        await session.commit()

        logger.info(
            "Payment SUCCESS: payment_id=%s order_id=%s",
            payment.id,
            payment.order_id,
        )

        return payment