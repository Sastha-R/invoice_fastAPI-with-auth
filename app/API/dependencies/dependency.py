from app.repositories.implementations.invoice_repository import InvoiceRepository
from app.repositories.implementations.user_repository import UserRepository
from app.services.implementations.auth_service import AuthService
from app.services.implementations.invoice_reports import InvoiceReports
from app.services.implementations.services import InvoiceService


def get_invoice_service():
    repository = InvoiceRepository()    
    return InvoiceService(repository)

def get_invoice_reportS():
    repository = InvoiceRepository()    
    return InvoiceReports(repository)

def get_auth_service() -> AuthService:
    user_repository = UserRepository()
    return AuthService(user_repository)