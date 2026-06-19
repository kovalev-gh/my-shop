from domains.base.exceptions import NotFoundException, AlreadyExistsException


class PaymentNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(
            detail="Payment not found",
        )


class PaymentAlreadySucceededException(AlreadyExistsException):

    def __init__(self) -> None:
        super().__init__(
            detail="Payment already exists",
        )