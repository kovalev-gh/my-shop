from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.postgres import get_async_session

from domains.auth.dependencies import get_current_user

from .models import User
from .schemas import UserRead
from .service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

service = UserService()


@router.get(
    "/me",
    response_model=UserRead,
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserRead,
)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    user = await service.get_by_id(
        session=session,
        user_id=user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_me(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await service.delete_user(
        session=session,
        user=current_user,
    )

    return None