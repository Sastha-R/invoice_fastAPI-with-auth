from alembic.util import status
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import decode_access_token
from app.database.database import get_db
from app.repository.invoice_repository.invoice_repository import InvoiceRepository
from app.repository.user_repository.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.invoice_service.services import InvoiceService
from app.services.invoice_service.invoice_reports import InvoiceReports

def get_invoice_service():
    repository = InvoiceRepository()    
    return InvoiceService(repository)

def get_invoice_reportS():
    repository = InvoiceRepository()    
    return InvoiceReports(repository)

def get_auth_service() -> AuthService:
    user_repository = UserRepository()
    return AuthService(user_repository)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (Exception):
        raise credentials_exception

    user_repository = UserRepository()
    user = await user_repository.get_by_id(db, user_id)

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user

