from fastapi import status


class DomainException(Exception):
    """Base class for all domain-specific exceptions."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class NotFoundException(DomainException):
    def __init__(self, resource: str):
        super().__init__(message=f"{resource} not found.", code="NOT_FOUND")


class ValidationException(DomainException):
    def __init__(self, message: str):
        super().__init__(message=message, code="VALIDATION_ERROR")


from fastapi.responses import JSONResponse


def domain_exception_handler(request, exc: DomainException):
    """Maps domain exceptions to HTTP responses for FastAPI."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    if isinstance(exc, NotFoundException):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, ValidationException):
        status_code = status.HTTP_400_BAD_REQUEST

    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )
