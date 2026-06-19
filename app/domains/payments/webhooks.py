import logging

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.postgres import get_async_session

from domains.payments.exceptions import PaymentNotFoundException
from domains.payments.service import PaymentService


router = APIRouter(
    prefix="/webhooks",
    tags=["Payment Webhooks"],
)

service = PaymentService()

logger = logging.getLogger(__name__)


@router.post("/fake")
async def fake_webhook(
    payload: dict,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Webhook от фейкового платёжного провайдера
    """

    logger.info("WEBHOOK RECEIVED: %s", payload)

    # 1. проверяем event
    event = payload.get("event")

    if event != "payment.succeeded":
        logger.info("WEBHOOK IGNORED: event=%s", event)
        return {"status": "ignored", "event": event}

    # 2. достаём provider_payment_id
    try:
        provider_payment_id = payload["object"]["id"]
        logger.info("Processing payment webhook: provider_payment_id=%s", provider_payment_id)

    except Exception as e:
        logger.error("INVALID WEBHOOK PAYLOAD: %s", payload)
        logger.exception(e)
        return {"status": "invalid_payload"}

    # 3. пробуем обновить payment
    try:
        payment = await service.mark_succeeded_by_provider_id(
            session=session,
            provider_payment_id=provider_payment_id,
        )

        logger.info(
            "PAYMENT UPDATED SUCCESSFULLY: payment_id=%s order_id=%s status=%s",
            payment.id,
            payment.order_id,
            payment.status,
        )

    except PaymentNotFoundException:
        logger.warning(
            "PAYMENT NOT FOUND for provider_payment_id=%s",
            provider_payment_id,
        )
        return {"status": "payment_not_found"}

    except Exception as e:
        logger.error("WEBHOOK PROCESSING ERROR")
        logger.exception(e)
        return {"status": "error"}

    return {"status": "ok"}