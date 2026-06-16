from domains.base.exceptions import (
    AlreadyExistsException,
    NotFoundException,
)


class UserAlreadyExistsException(
    AlreadyExistsException,
):
    def __init__(self) -> None:
        super().__init__(
            detail="User with this email already exists",
        )