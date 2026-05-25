from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db.postgres import Base

if TYPE_CHECKING:
    from .product import Product
    from .order_item import OrderItem


class Order(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    promocode: Mapped[str | None] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )
