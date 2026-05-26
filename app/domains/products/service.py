# app/domains/products/service.py

from sqlalchemy.ext.asyncio import AsyncSession

from domains.base.service import BaseService

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

    async def create_product(
        self,
        session: AsyncSession,
        product_in: ProductCreate,
    ) -> Product:

        product = await self.create(
            session=session,
            data=product_in.model_dump(),
        )

        return product

    async def update_product(
        self,
        session: AsyncSession,
        product: Product,
        product_update: ProductUpdate | ProductUpdatePartial,
        partial: bool = False,
    ) -> Product:

        updated_product = await self.update(
            session=session,
            obj=product,
            data=product_update.model_dump(
                exclude_unset=partial,
            ),
        )

        return updated_product

    async def delete_product(
        self,
        session: AsyncSession,
        product: Product,
    ) -> None:

        await self.delete(
            session=session,
            obj=product,
        )