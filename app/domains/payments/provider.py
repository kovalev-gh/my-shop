from uuid import uuid4
from decimal import Decimal
from yookassa import Configuration, Payment

class FakePaymentProvider:

    async def create_payment(
        self,
        amount: Decimal,
        order_id: int,
    ) -> dict:

        return {
            "id": str(uuid4()),
            "status": "pending",
            "confirmation_url": (
                f"http://localhost:8000/payments/fake-success/"
                f"{uuid4()}"
            ),
        }

class YookassaPaymentProvider:

    def __init__(self, shop_id: str, secret_key: str):
        Configuration.account_id = shop_id
        Configuration.secret_key = secret_key

    async def create_payment(self, amount: Decimal, order_id: int) -> dict:
        idempotence_key = str(uuid.uuid4())

        payment = Payment.create(
            {
                "amount": {
                    "value": f"{amount:.2f}",
                    "currency": "RUB",
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "http://localhost:8000/payments/success",
                },
                "capture": True,
                "description": f"Order #{order_id}",
                "metadata": {
                    "order_id": order_id,
                },
            },
            idempotence_key,
        )

        return {
            "id": payment.id,
            "status": payment.status,
            "confirmation_url": payment.confirmation.confirmation_url,
        }