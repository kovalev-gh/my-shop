# app/domains/products/router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.postgres import get_async_session

from .dependencies import get_product_by_id
from .models import Product
from .schemas import (
    ProductCreate,
    ProductRead,
    ProductUpdate,
    ProductUpdatePartial,
)
from .service import ProductService


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

service = ProductService()


@router.get(
    "/",
    response_model=list[ProductRead],
)
async def get_products(
    session: AsyncSession = Depends(get_async_session),
):

    return await service.get_all(
        session=session,
    )


@router.get(
    "/{product_id}/",
    response_model=ProductRead,
)
async def get_product(
    product: Product = Depends(get_product_by_id),
):

    return product


@router.post(
    "/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(get_async_session),
):

    return await service.create_product(
        session=session,
        product_in=product_in,
    )


@router.patch(
    "/{product_id}/",
    response_model=ProductRead,
)
async def update_product_partial(
    product_update: ProductUpdatePartial,
    product: Product = Depends(get_product_by_id),
    session: AsyncSession = Depends(get_async_session),
):

    return await service.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True,
    )


@router.delete(
    "/{product_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    product: Product = Depends(get_product_by_id),
    session: AsyncSession = Depends(get_async_session),
):

    await service.delete_product(
        session=session,
        product=product,
    )