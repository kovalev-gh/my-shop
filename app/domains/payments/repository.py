from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domains.base.repository import BaseRepository

from .models import Payment


class PaymentRepository(
    BaseRepository[Payment],
):
    model = Payment

    async def get_by_provider_payment_id(
        self,
        session: AsyncSession,
        provider_payment_id: str,
    ) -> Payment | None:

        stmt = select(Payment).where(
            Payment.provider_payment_id == provider_payment_id,
        )

        result = await session.execute(stmt)

        return result.scalar_one_or_none()