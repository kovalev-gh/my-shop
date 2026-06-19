from domains.base.exceptions import NotFoundException, AlreadyExistsException


class PaymentNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(
            detail="Payment not found",
        )

class PaymentAlreadyExistsException(AlreadyExistsException):
    def __init__(self) -> None:
        super().__init__(detail="Payment already exists"
        )

class PaymentAlreadySucceededException(AlreadyExistsException):
    def __init__(self) -> None:
        super().__init__(
            detail="Payment already succeeded",
        )

class PaymentAlreadyCanceledException(AlreadyExistsException):
    def __init__(self) -> None:
        super().__init__(
            detail="Payment was canceled and cannot be recreated for this order",
        )