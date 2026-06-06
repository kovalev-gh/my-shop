# app/domains/products/service.py

from sqlalchemy.ext.asyncio import AsyncSession

from domains.base.service import BaseService

from .exceptions import ProductNotFoundException
from .models import Product
from .repository import ProductRepository
from .schemas import (
    ProductCreate,
    ProductUpdate,
    ProductUpdatePartial,
)


class ProductService(
    BaseService[
        Product,
        ProductRepository,
    ]
):
    repository_class = ProductRepository

    async def get_product(
        self,
        session: AsyncSession,
        product_id: int,
    ) -> Product:

        product = await self.get_by_id(
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

        return await self.create(
            session=session,
            **product_in.model_dump(),
        )

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

        return await self.update(
            session=session,
            obj=product,
            **product_update.model_dump(
                exclude_unset=partial,
            ),
        )

    async def delete_product(
        self,
        session: AsyncSession,
        product_id: int,
    ) -> None:

        product = await self.get_product(
            session=session,
            product_id=product_id,
        )

        await self.delete(
            session=session,
            obj=product,
        )