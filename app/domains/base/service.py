# app/domains/base/service.py

from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.postgres import Base
from domains.base.repository import BaseRepository


ModelType = TypeVar("ModelType", bound=Base)

RepositoryType = TypeVar(
    "RepositoryType",
    bound=BaseRepository,
)


class BaseService(
    Generic[
        ModelType,
        RepositoryType,
    ]
):
    repository_class: type[RepositoryType]

    def __init__(self):

        self.repository = self.repository_class()

    async def get_all(
        self,
        session: AsyncSession,
    ) -> list[ModelType]:

        return await self.repository.get_all(
            session=session,
        )

    async def get_by_id(
        self,
        session: AsyncSession,
        obj_id: int,
    ) -> ModelType | None:

        return await self.repository.get_by_id(
            session=session,
            obj_id=obj_id,
        )

    async def create(
        self,
        session: AsyncSession,
        **kwargs,
    ) -> ModelType:

        obj = await self.repository.create(
            session=session,
            **kwargs,
        )

        await session.commit()

        return obj

    async def update(
        self,
        session: AsyncSession,
        obj: ModelType,
        **kwargs,
    ) -> ModelType:

        obj = await self.repository.update(
            session=session,
            obj=obj,
            **kwargs,
        )

        await session.commit()

        return obj

    async def delete(
        self,
        session: AsyncSession,
        obj: ModelType,
    ) -> None:

        await self.repository.delete(
            session=session,
            obj=obj,
        )

        await session.commit()