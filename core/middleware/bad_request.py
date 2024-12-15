import logging
from typing import Union
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from sqlalchemy.exc import PendingRollbackError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("Middleware started")


async def validation_exception_handler(
    _: Request,
    exc: Union[RequestValidationError, Exception, PendingRollbackError],
) -> JSONResponse:
    errors: dict[str, list[str]] = {}
    if isinstance(exc, RequestValidationError):
        for err in exc.errors():
            field = err["loc"][-1]
            if field not in errors:
                errors[field] = []

    elif isinstance(exc, ValueError):
        return JSONResponse(
            status_code=400,
            content={"detail": f"ValueError: {str(exc)}"},
        )

    return JSONResponse(
        status_code=422,
        content={"detail": errors},
    )


async def validation_unique_handler(
    _: Request,
    exc: Union[RequestValidationError, Exception, PendingRollbackError],
) -> JSONResponse:
    errors: dict[str, list[str]] = {}
    if (
        isinstance(exc, PendingRollbackError) and exc.code == "7s2a"
    ):  # 7s2a is the code for "PendingRollbackError"
        return JSONResponse(
            status_code=400,
            content={"detail": "unique value constraint violated"},
        )

    return JSONResponse(
        status_code=422,
        content={"detail": errors},
    )


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except StarletteHTTPException as exc:
            return JSONResponse(
                {"detail": exc.detail},
                status_code=exc.status_code,
                headers=exc.headers,
            )
        except Exception as exc:
            return JSONResponse({"detail": str(exc)}, status_code=400)
