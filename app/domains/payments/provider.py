from uuid import uuid4


class FakePaymentProvider:

    async def create_payment(
        self,
        amount: float,
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