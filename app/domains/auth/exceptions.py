# domains/auth/exceptions.py

class AuthException(Exception):
    detail = "Authentication error"

    def __init__(self, detail: str | None = None):
        self.detail = detail or self.detail
        super().__init__(self.detail)


class InvalidCredentialsException(AuthException):
    detail = "Invalid email or password"


class InvalidTokenException(AuthException):
    detail = "Invalid token"


class InvalidTokenTypeException(AuthException):
    detail = "Invalid token type"


class UserNotFoundException(AuthException):
    detail = "User not found"