# app/domains/products/schemas.py

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    title: str
    description: str
    unit_price: float
    stock_quantity: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductUpdatePartial(BaseModel):
    title: str | None = None
    description: str | None = None
    unit_price: float | None = None
    stock_quantity: int | None = None


class ProductRead(ProductBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int