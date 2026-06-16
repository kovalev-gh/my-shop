from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from domains.auth.security import hash_password

from .models import User
from .repository import UserRepository
from .schemas import UserCreate, UserUpdate, UserUpdatePartial
from .exceptions import UserAlreadyExistsException


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

        user = User(
            email=user_in.email,
            hashed_password=hash_password(user_in.password),
        )

        session.add(user)

        try:
            await session.commit()
            await session.refresh(user)
            return user

        except IntegrityError:
            await session.rollback()
            raise UserAlreadyExistsException()

    async def update_user(
            self,
            session: AsyncSession,
            user_id: int,
            user_update: UserUpdate | UserUpdatePartial,
            partial: bool = False,
    ) -> User:

        user = await self.get_by_id(
            session=session,
            user_id=user_id,
        )

        try:
            user = await self.repository.update(
                session=session,
                obj=user,
                **user_update.model_dump(exclude_unset=partial),
            )

            await session.commit()
            await session.refresh(user)
            return user

        except IntegrityError:
            await session.rollback()
            raise UserAlreadyExistsException()

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