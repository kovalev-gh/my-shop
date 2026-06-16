# app/domains/products/service.py

from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import ProductNotFoundException
from .models import Product
from .repository import ProductRepository
from .schemas import (
    ProductCreate,
    ProductUpdate,
    ProductUpdatePartial,
)

import logging

logger = logging.getLogger(__name__)


class ProductService:

    def __init__(self):
        self.repository = ProductRepository()

    async def get_all(
        self,
        session: AsyncSession,
    ) -> list[Product]:

        return await self.repository.get_all(
            session=session,
        )

    async def get_product(
        self,
        session: AsyncSession,
        product_id: int,
    ) -> Product:

        product = await self.repository.get_by_id(
            session=session,
            obj_id=product_id,
        )

        if product is None:
            raise ProductNotFoundException()

        return product

    async def create_product(
        self,
        session: AsyncSession,
        product_in: ProductCreate,
    ) -> Product:

        logger.info(
            "Creating product: %s",
            product_in.title,
        )

        product = await self.repository.create(
            session=session,
            **product_in.model_dump(),
        )

        await session.commit()

        logger.info(
            "Product created: id=%s",
            product.id,
        )

        return product

    async def update_product(
        self,
        session: AsyncSession,
        product_id: int,
        product_update: ProductUpdate | ProductUpdatePartial,
        partial: bool = False,
    ) -> Product:

        product = await self.get_product(
            session=session,
            product_id=product_id,
        )

        product = await self.repository.update(
            session=session,
            obj=product,
            **product_update.model_dump(
                exclude_unset=partial,
            ),
        )

        await session.commit()

        return product

    async def delete_product(
        self,
        session: AsyncSession,
        product_id: int,
    ) -> None:

        product = await self.get_product(
            session=session,
            product_id=product_id,
        )

        await self.repository.delete(
            session=session,
            obj=product,
        )

        await session.commit()