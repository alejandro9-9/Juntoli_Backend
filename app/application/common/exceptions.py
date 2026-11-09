class ApplicationError(Exception):
    """Base error raised by application use cases."""


class ApplicationValidationError(ApplicationError, ValueError):
    """Raised when input violates an application rule."""


class EntityNotFoundError(ApplicationError):
    pass


class ConflictError(ApplicationError):
    pass


class AuthorizationError(ApplicationError):
    pass


class InvalidStateError(ApplicationError):
    pass
