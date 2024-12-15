import logging
from typing import Union
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from sqlalchemy.exc import PendingRollbackError

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
