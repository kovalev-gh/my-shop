from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from .models import PaymentStatus


class PaymentRead(BaseModel):
    id: int
    order_id: int
    provider: str
    provider_payment_id: str
    amount: Decimal
    status: PaymentStatus
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class CreatePaymentResponse(BaseModel):
    payment_id: int
    payment_url: str