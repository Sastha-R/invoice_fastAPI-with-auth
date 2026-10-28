import pytest
from sqlalchemy import inspect, text

from app.database.base import Base
from app.models.user_models import User
from app.models.models import Invoice, InvoiceFile


@pytest.mark.asyncio
async def test_test_database_connection(setup_test_database, db_session):
    result = await db_session.execute(text("SELECT 1"))
    assert result.scalar_one() == 1


@pytest.mark.asyncio
async def test_required_tables_exist(setup_test_database):
    from conftest import test_engine

    async with test_engine.connect() as connection:
        def get_table_names(sync_connection):
            return inspect(sync_connection).get_table_names()

        table_names = await connection.run_sync(get_table_names)

    assert "users" in table_names
    assert "invoices" in table_names
    assert "invoice_files" in table_names