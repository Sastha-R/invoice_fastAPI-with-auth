import logging

from fastapi import FastAPI, Request, logger
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import InvoiceAlreadyExistsError, InvoiceNotFoundError
from app.API.routes.route import invoice_router
from app.API.routes.cookies import cookie_router
from sqlalchemy.exc import SQLAlchemyError
from app.API.routes.reports import report_route
from app.API.routes.auth import auth_router
import time

app = FastAPI(title="Invoice Management CRUD API")

    
app.include_router(invoice_router)
app.include_router(report_route)
app.include_router(cookie_router)
app.include_router(auth_router)



@app.exception_handler(InvoiceNotFoundError)
def invoice_not_found_handler(request: Request, exc: InvoiceNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": str(exc)})


@app.exception_handler(InvoiceAlreadyExistsError)
def invoice_already_exists_handler(request: Request, exc: InvoiceAlreadyExistsError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"message": str(exc)})


@app.exception_handler(SQLAlchemyError)
def  sqlalchemy_error_handler(request : Request , exc : SQLAlchemyError) -> JSONResponse:
    return JSONResponse(status_code=500 , content={"message": str(exc)})



logging.basicConfig(
    filename="app_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

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