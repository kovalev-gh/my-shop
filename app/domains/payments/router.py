from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.postgres import get_async_session

from .schemas import (
    PaymentRead,
    CreatePaymentResponse,
)
from .service import PaymentService


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)

service = PaymentService()


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
    return await service.get_payment(
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
    return await service.mark_succeeded(
        session=session,
        payment_id=payment_id,
    )