from domains.base.exceptions import (
    AlreadyExistsException,
    NotFoundException,
)


class ProductNotFoundException(NotFoundException):
    def __init__(self) -> None:
        super().__init__(
            detail="Product not found",
        )


class ProductAlreadyExistsException(
    AlreadyExistsException,
):
    def __init__(self) -> None:
        super().__init__(
            detail="Product already exists",
        )