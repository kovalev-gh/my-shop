from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from typing import TYPE_CHECKING

from core.db.postgres import get_async_session
from domains.users.repository import UserRepository

if TYPE_CHECKING:
    from domains.orders.models import Order
    pass
from domains.users.models import User

from .jwt import decode_jwt


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)

user_repository = UserRepository()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_jwt(token)

        token_type = payload.get("type")
        user_id = payload.get("sub")

        if token_type != "access":
            raise credentials_exception

        if user_id is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    user = await user_repository.get_by_id(
        session=session,
        obj_id=int(user_id),
    )

    if user is None:
        raise credentials_exception

    return user