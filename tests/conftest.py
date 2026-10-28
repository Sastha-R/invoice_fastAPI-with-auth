import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.database.base import Base
from app.database.database import get_db
from app.main import app
# from app.models.user_models import User
# from app.models.models import Invoice, InvoiceFile
from app.config import settings


TEST_DATABASE_URL = settings.database_url().replace(
    f"/{settings.db_name}",
    "/invoice_testing"
)

if not TEST_DATABASE_URL.endswith("/invoice_testing"):
    raise RuntimeError("Use the test database for testing")

test_engine = create_async_engine(TEST_DATABASE_URL)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False
)


@pytest_asyncio.fixture(scope="function", loop_scope="function")
async def setup_test_database():
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


@pytest_asyncio.fixture
async def db_session(setup_test_database):
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
def override_get_db(db_session):
    async def _get_test_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_test_db

    yield

    app.dependency_overrides.pop(get_db, None)


@pytest_asyncio.fixture
async def client(override_get_db):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as test_client:
        yield test_client