from sqlalchemy.ext.asyncio import AsyncSession

from domains.users.models import User
from domains.users.repository import UserRepository

from .exceptions import InvalidCredentialsException
from .jwt import (
    create_access_token,
    create_refresh_token,
)
from .schemas import TokenResponse
from .security import validate_password


class AuthService:

    def __init__(self):
        self.user_repository = UserRepository()

    def create_tokens(
        self,
        user_id: int,
    ) -> TokenResponse:

        return TokenResponse(
            access_token=create_access_token(
                user_id=user_id,
            ),
            refresh_token=create_refresh_token(
                user_id=user_id,
            ),
        )

    async def authenticate_user(
        self,
        session: AsyncSession,
        email: str,
        password: str,
    ) -> User | None:

        user = await self.user_repository.get_by_email(
            session=session,
            email=email,
        )

        if user is None:
            return None

        if not validate_password(
            password=password,
            hashed_password=user.hashed_password,
        ):
            return None

        return user

    async def login(
        self,
        session: AsyncSession,
        email: str,
        password: str,
    ) -> TokenResponse:

        user = await self.authenticate_user(
            session=session,
            email=email,
            password=password,
        )

        if user is None:
            raise InvalidCredentialsException()

        return self.create_tokens(
            user_id=user.id,
        )