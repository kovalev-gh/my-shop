# app/domains/users/repository.py
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from domains.base.repository import BaseRepository
from .models import User

class UserRepository(BaseRepository[User],
):
    model = User
    async def get_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> User | None:

        stmt = select(User).where(
            User.email == email,
        )

        result = await session.execute(stmt)

        return result.scalar_one_or_none()