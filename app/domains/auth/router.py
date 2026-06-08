from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.postgres import get_async_session

from domains.users.models import User
from domains.users.schemas import UserCreate, UserRead
from domains.users.service import UserService

from .dependencies import get_current_user
from .exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
)
from .jwt import decode_jwt
from .schemas import (
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
)
from .service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

auth_service = AuthService()
user_service = UserService()


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    user = await user_service.create_user(
        session=session,
        user_in=user_in,
    )

    return auth_service.create_tokens(
        user_id=user.id,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await auth_service.login(
            session=session,
            email=form_data.username,
            password=form_data.password,
        )

    except InvalidCredentialsException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.detail,
        )


@router.post(
    "/login-json",
    response_model=TokenResponse,
)
async def login_json(
    credentials: LoginRequest,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await auth_service.login(
            session=session,
            email=credentials.email,
            password=credentials.password,
        )

    except InvalidCredentialsException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.detail,
        )


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
async def refresh_token(
    data: RefreshTokenRequest,
):
    try:
        payload = decode_jwt(
            data.refresh_token,
        )

        if payload.get("type") != "refresh":
            raise InvalidTokenException(
                "Invalid token type",
            )

        user_id = int(
            payload["sub"],
        )

        return auth_service.create_tokens(
            user_id=user_id,
        )

    except InvalidTokenException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.detail,
        )

    except (
        InvalidTokenError,
        KeyError,
        ValueError,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


@router.get(
    "/me",
    response_model=UserRead,
)
async def get_me(
    current_user: User = Depends(
        get_current_user,
    ),
):
    return current_user


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout():
    return None