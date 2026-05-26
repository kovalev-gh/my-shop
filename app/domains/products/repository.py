# app/domains/products/repository.py

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.base.repository import BaseRepository

from .models import Product


class ProductRepository(
    BaseRepository[Product],
):
    model = Product

    async def get_product_by_id(
        self,
        session: AsyncSession,
        product_id: int,
    ) -> Product | None:

        return await self.get_by_id(
            session=session,
            obj_id=product_id,
        )