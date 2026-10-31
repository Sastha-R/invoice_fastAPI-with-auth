from datetime import date
from decimal import Decimal
import pytest
from app.repositories.implementations.invoice_repository import InvoiceRepository
from app.schemas.invoice_schema import InvoiceData
from app.models.invoice_model import Invoice


@pytest.mark.asyncio
async def test_create_invoice(db_session):
    repository = InvoiceRepository()

    invoice_data = InvoiceData(
        invoice_number="TEST_001",
        customer_name="Sample Customer",
        customer_email="samplecustomer@example.com",
        invoice_date=date(2026, 10, 29),
        product_name="Mouse",
        quantity=2,
        unit_price=Decimal("1000.00"),
        discount_percentage=Decimal("5.00"),
        discount_amount=Decimal("100.00"),
        tax_percentage=Decimal("18.00"),
        tax_amount=Decimal("342.00"),
        subtotal=Decimal("2000.00"),
        taxable_amount=Decimal("1900.00"),
        total_amount=Decimal("2242.00"),
    )

    created_invoice = await repository.create(db_session, invoice_data)

    saved_invoice = await repository.get_by_invoice_number(
        db_session,
        "TEST_001",
    )


    assert created_invoice["invoice_number"] == "TEST_001"
    assert saved_invoice is not None
    assert saved_invoice.customer_name == "Sample Customer"
    assert saved_invoice.total_amount == Decimal("2242.00")

# python -m pytest tests/integration_test/test_invoice_repository.py -v
