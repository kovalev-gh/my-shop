from domains.base.exceptions import (
    BadRequestException,
    NotFoundException,
)


class OrderNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(
            detail="Order not found",
        )


class NotEnoughStockException(
    BadRequestException,
):
    def __init__(
        self,
        product_id: int,
    ):
        super().__init__(
            detail=f"Not enough stock for product {product_id}",
        )

class OrderItemNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(
            detail="Order item not found",
        )