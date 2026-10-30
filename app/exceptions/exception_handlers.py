from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions.custom_exceptions import (
    InvoiceAlreadyExistsError,
    InvoiceNotFoundError,
)
from app.core.logging_config import logger


async def invoice_not_found_handler(
            request: Request,
            exc: InvoiceNotFoundError,
        ) -> JSONResponse:
    logger.warning(
        f"Invoice not found: {request.method} {request.url.path} - {str(exc)}"
    )

    return JSONResponse(
        status_code=404,
        content={"message": str(exc)},
    )


async def invoice_already_exists_handler(
            request: Request,
            exc: InvoiceAlreadyExistsError,
        ) -> JSONResponse:
    logger.warning(
        f"Invoice already exists: {request.method} {request.url.path} - {str(exc)}"
    )

    return JSONResponse(
        status_code=409,
        content={"message": str(exc)},
    )


async def sqlalchemy_error_handler(
            request: Request,
            exc: SQLAlchemyError,
        ) -> JSONResponse:
    logger.error(
        f"Database error: {request.method} {request.url.path} - {str(exc)}",
    )

    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )

async def general_exception_handler(
            request: Request,
            exc: Exception,
        ) -> JSONResponse:
    logger.error(
        "Unexpected error: %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred"},
    )