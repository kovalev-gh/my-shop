# app/domains/users/service.py

from sqlalchemy.ext.asyncio import AsyncSession

from domains.auth.security import hash_password

from .models import User
from .repository import UserRepository
from .schemas import UserCreate


class UserService:

    def __init__(self):
        self.repository = UserRepository()

    async def get_by_id(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> User | None:

        return await self.repository.get_by_id(
            session=session,
            obj_id=user_id,
        )

    async def get_by_email(
        self,
        session: AsyncSession,
        email: str,
    ) -> User | None:

        return await self.repository.get_by_email(
            session=session,
            email=email,
        )

    async def create_user(
        self,
        session: AsyncSession,
        user_in: UserCreate,
    ) -> User:

        user = await self.repository.create(
            session=session,
            email=user_in.email,
            hashed_password=hash_password(
                user_in.password,
            ),
        )

        await session.commit()

        return user

    async def delete_user(
        self,
        session: AsyncSession,
        user: User,
    ) -> None:

        await self.repository.delete(
            session=session,
            obj=user,
        )

        await session.commit()