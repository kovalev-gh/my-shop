# app/domains/products/dependencies.py

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.postgres import get_async_session

from .models import Product
from .service import ProductService


service = ProductService()


async def get_product_by_id(
    product_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Product:

    product = await service.get_by_id(
        session=session,
        obj_id=product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product