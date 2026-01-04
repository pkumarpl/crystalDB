"""Custom exceptions for CrystalDB."""


class CrystalDBException(Exception):
    """Base exception for CrystalDB."""

    def __init__(self, message: str, code: str | None = None) -> None:
        self.message = message
        self.code = code or self.__class__.__name__
        super().__init__(self.message)


class DatabaseException(CrystalDBException):
    """Database-related exceptions."""

    pass


class ValidationException(CrystalDBException):
    """Data validation exceptions."""

    pass


class NotFoundException(CrystalDBException):
    """Resource not found exceptions."""

    pass


class AuthenticationException(CrystalDBException):
    """Authentication-related exceptions."""

    pass


class AuthorizationException(CrystalDBException):
    """Authorization-related exceptions."""

    pass
