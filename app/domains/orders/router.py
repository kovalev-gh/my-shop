# app/domains/orders/router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.postgres import get_async_session

from domains.auth.dependencies import get_current_user
from domains.users.models import User

from .schemas import (
    OrderCreate,
    OrderRead,
)
from .service import OrderService


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

service = OrderService()


@router.get(
    "/",
    response_model=list[OrderRead],
)
async def get_my_orders(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_user_orders(
        session=session,
        user_id=current_user.id,
    )


@router.get(
    "/all",
    response_model=list[OrderRead],
)
async def get_all_orders(
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_all_orders(
        session=session,
    )


@router.get(
    "/{order_id}",
    response_model=OrderRead,
)
async def get_order(
    order_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_order(
        session=session,
        order_id=order_id,
    )


@router.post(
    "/",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order_in: OrderCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.create_order(
        session=session,
        user_id=current_user.id,
        order_in=order_in,
    )

@router.post(
    "/{order_id}/items",
    response_model=OrderRead,
)
async def add_item(
    order_id: int,
    product_id: int,
    quantity: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await service.add_item_to_order(
        session=session,
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
    )

@router.delete(
    "/{order_id}/items/{item_id}",
    response_model=OrderRead,
)
async def remove_item(
    order_id: int,
    item_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await service.remove_item_from_order(
        session=session,
        order_id=order_id,
        item_id=item_id,
    )
@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_order(
    order_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await service.delete_order(
        session=session,
        order_id=order_id,
    )