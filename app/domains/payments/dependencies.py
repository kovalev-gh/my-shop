from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.postgres import get_async_session

from domains.auth.dependencies import get_current_user
from domains.users.models import User

from .models import Payment
from .service import PaymentService


service = PaymentService()


async def get_payment_with_access(
    payment_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
) -> Payment:
    payment = await service.get_payment_by_id(
        session=session,
        payment_id=payment_id,
    )

    if (
        payment.order.user_id != current_user.id
        and not current_user.is_admin
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return payment