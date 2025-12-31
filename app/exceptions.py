from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException



class AppException(Exception):
    """
    Base class for application-level exceptions.
    Extend this for various custom error types.
    """
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotAllowedException(AppException):
    def __init__(self, message="Operation not allowed"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class ResourceNotFoundException(AppException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)



async def app_exception_handler(request: Request, exc: AppException):
    """
    Handles custom business exceptions.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "request_id": getattr(request.state, "request_id", None),
        },
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handles standard HTTP exceptions.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "request_id": getattr(request.state, "request_id", None),
        },
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles pydantic validation errors in request body/query params/path params.
    """
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "details": exc.errors(),
            "body": exc.body,
            "request_id": getattr(request.state, "request_id", None),
        },
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    Fallback handler — catches all unexpected exceptions.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "request_id": getattr(request.state, "request_id", None),
        },
    )



def setup_exception_handlers(app: FastAPI):
    """
    Register all custom and system exception handlers.
    """
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    # Fallback for unexpected errors
    app.add_exception_handler(Exception, unhandled_exception_handler)