# import logging
# from fastapi import FastAPI, Request, logger
from fastapi import FastAPI, Request
from app.core.logging_config import logger
from fastapi.responses import JSONResponse
from app.API.routes.route import invoice_router
from app.API.routes.cookies import cookie_router
from sqlalchemy.exc import SQLAlchemyError
from app.API.routes.reports import report_route
from app.API.routes.auth import auth_router
import time
from app.exceptions.custom_exceptions import InvoiceAlreadyExistsError, InvoiceNotFoundError
from app.exceptions.exception_handlers import (
    invoice_not_found_handler,
    invoice_already_exists_handler,
    sqlalchemy_error_handler,
    general_exception_handler
)


app = FastAPI(title="Invoice Management CRUD API")
app.add_exception_handler(
    InvoiceNotFoundError,
    invoice_not_found_handler,
)

app.add_exception_handler(
    InvoiceAlreadyExistsError,
    invoice_already_exists_handler,
)

app.add_exception_handler(
    SQLAlchemyError,
    sqlalchemy_error_handler,
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)
    
app.include_router(invoice_router)
app.include_router(report_route)
app.include_router(cookie_router)
app.include_router(auth_router)



@app.middleware("http")
async def log_request_middleware(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f} seconds"
    )


    return response