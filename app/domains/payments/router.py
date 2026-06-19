from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.postgres import get_async_session

from .schemas import PaymentRead, CreatePaymentResponse
from .service import PaymentService
from .provider import FakePaymentProvider


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)

service = PaymentService()
provider = FakePaymentProvider()


@router.post(
    "/orders/{order_id}",
    response_model=CreatePaymentResponse,
)
async def create_payment(
    order_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    payment, payment_url = await service.create_payment(
        session=session,
        order_id=order_id,
    )

    return {
        "payment_id": payment.id,
        "payment_url": payment_url,
    }


@router.get(
    "/{payment_id}",
    response_model=PaymentRead,
)
async def get_payment(
    payment_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_payment_by_id(
        session=session,
        payment_id=payment_id,
    )


@router.post(
    "/{payment_id}/success",
    response_model=PaymentRead,
)
async def success_payment(
    payment_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await service.mark_succeeded_by_payment_id(
        session=session,
        payment_id=payment_id,
    )


@router.get("/fake-pay/{provider_payment_id}")
async def fake_pay(
    provider_payment_id: str,
):
    """
    Симуляция "нажатия кнопки оплатить"
    → провайдер сам отправляет webhook
    """

    await provider.send_success_webhook(provider_payment_id)

    return {
        "status": "success",
        "message": "Webhook sent via fake provider",
    }