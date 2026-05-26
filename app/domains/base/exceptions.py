# app/domains/base/exceptions.py
# не уверен, что этот файл вообще нужен


class DomainException(Exception):
    """
    Базовое доменное исключение.

    Все бизнес-ошибки должны наследоваться от него.
    """

    default_detail = "Domain exception"

    def __init__(
        self,
        detail: str | None = None,
    ):

        self.detail = detail or self.default_detail

        super().__init__(self.detail)


class NotFoundException(DomainException):
    """
    Объект не найден.
    """

    default_detail = "Object not found"


class ValidationException(DomainException):
    """
    Ошибка бизнес-валидации.
    """

    default_detail = "Validation error"


class AlreadyExistsException(DomainException):
    """
    Объект уже существует.
    """

    default_detail = "Object already exists"


class PermissionDeniedException(DomainException):
    """
    Недостаточно прав.
    """

    default_detail = "Permission denied"