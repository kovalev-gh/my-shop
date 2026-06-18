from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.postgres import get_async_session
from domains.payments.exceptions import PaymentNotFoundException
from domains.payments.service import PaymentService


router = APIRouter(
    prefix="/webhooks",
    tags=["Payment Webhooks"],
)

service = PaymentService()


@router.post("/fake_yookassa")
async def fake_yookassa_webhook(
    payload: dict,
):
    print(payload)

    return {
        "status": "ok",
    }


@router.post("/test_yookassa")
async def test_yookassa_webhook(
    payload: dict,
    session: AsyncSession = Depends(get_async_session),
):
    if payload.get("event") != "payment.succeeded":
        return {"status": "ignored"}

    await service.mark_succeeded_by_provider_id(
        session=session,
        provider_payment_id=payload["object"]["id"],
    )

    return {"status": "ok"}