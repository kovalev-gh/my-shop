from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Integer,
    Float,
    Numeric,
    String,
    DateTime,
    func,
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



class Order(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    promocode: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
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

class OrderItem(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product")
