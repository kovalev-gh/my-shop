from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    String,
    DateTime,
    Numeric,
    func,
    Enum as SQLEnum,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from core.db.postgres import Base


if TYPE_CHECKING:
    from domains.orders.models import Order


class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    CANCELED = "canceled"


class Payment(Base):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False, default="yookassa")
    provider_payment_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(SQLEnum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), default=datetime.utcnow)

    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="payments",
    )