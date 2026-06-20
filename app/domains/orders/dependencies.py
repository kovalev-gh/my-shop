# app/domains/orders/dependencies.py

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.postgres import get_async_session
from domains.auth.dependencies import get_current_user
from domains.users.models import User

from .models import Order
from .service import OrderService


service = OrderService()


async def get_order_with_access(
    order_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
) -> Order:
    order = await service.get_order(
        session=session,
        order_id=order_id,
    )

    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return order