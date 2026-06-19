from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from enum import Enum

from sqlalchemy import (
    ForeignKey,
    Integer,
    Float,
    Numeric,
    String,
    DateTime,
    func,
    Enum as SQLEnum
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from core.db.postgres import Base


if TYPE_CHECKING:
    from domains.users.models import User
    from domains.products.models import Product
    from domains.payments.models import Payment



class OrderStatus(str, Enum):
    CREATED = "created"
    WAITING_PAYMENT = "waiting_payment"
    PAID = "paid"
    CANCELED = "canceled"

class Order(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    promocode: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus),
        nullable=False,
        default=OrderStatus.CREATED,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="orders",
    )
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )
    payments: Mapped[list["Payment"]] = relationship(
        "Payment",
        back_populates="order",
        cascade="all, delete-orphan",
    )

class OrderItem(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product")
