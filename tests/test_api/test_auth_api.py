import pytest


@pytest.mark.asyncio
async def test_register_user(client):
    user_data = {
        "username": "testuser",
        "email": "testuser@gmail.com",
        "password": "Password@123"
    }

    response = await client.post("/auth/register", json=user_data)

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["username"] == user_data["username"]
    assert response_data["email"] == user_data["email"]
    assert "id" in response_data
    assert "password" not in response_data

    # python -m pytest .\tests\test_api\test_auth_api.py 