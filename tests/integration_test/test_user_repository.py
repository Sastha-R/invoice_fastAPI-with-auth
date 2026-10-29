import pytest
from app.models.user_models import User
from app.repositories.implementations.user_repository import UserRepository


@pytest.mark.asyncio
async def test_create_user(db_session):
    repository = UserRepository()

    user_data = {
        "username": "testuser",
        "email": "testuser@gmail.com",
        "password": "testpasssword",
        "role": "employee",
        "is_active": True,
    }

    created_user = await repository.create(db_session, user_data)

    assert created_user.id is not None
    assert created_user.username == "testuser"
    assert created_user.email == "testuser@gmail.com"
    assert created_user.role == "employee"
    
