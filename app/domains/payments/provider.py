import logging
from decimal import Decimal
from uuid import uuid4
from core.config import settings

import httpx

logger = logging.getLogger(__name__)

class FakePaymentProvider:
    """
    Фейковый платёжный провайдер:
    - создаёт payment intent
    - имитирует успешную оплату через webhook
    """

    def __init__(self):
        self.base_url = f"http://localhost:8000"

    async def create_payment(
        self,
        amount: Decimal,
        order_id: int,
    ) -> dict:
        """
        Создание "платёжного интента" у провайдера
        (в реальности это Stripe/YooKassa create intent)
        """

        provider_payment_id = str(uuid4())

        confirmation_url = f"{self.base_url}/payments/fake-pay/{provider_payment_id}"

        logger.info("confirmation_url: %s",confirmation_url)
        return {
            "id": provider_payment_id,
            "status": "pending",
            "confirmation_url": confirmation_url
        }

    async def send_success_webhook(self, provider_payment_id: str) -> None:
        """
        ИМИТАЦИЯ:
        внешний платёжный сервис сообщает об успешной оплате
        """

        async with httpx.AsyncClient() as client:
            await client.post(
                    f"{self.base_url}/webhooks/fake",
                json={
                    "event": "payment.succeeded",
                    "object": {
                        "id": provider_payment_id,
                    },
                },
                timeout=5.0,
            )