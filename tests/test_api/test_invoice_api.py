import pytest

async def create_employee_and_get_token(client):
    user_data = {
    "username": "testuser",
    "email": "testuser@gmail.com",
    "password": "Password@123",
    }

    register_response = await client.post(
        "/auth/register",
        json=user_data,

    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/auth/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]



def invoice_payload():

    return {
    "invoice_number": "IN_001",
    "customer_name": "Test Customer",
    "customer_email": "customer@gmail.com",
    "invoice_date": "2026-10-30",
    "product_name": "Laptop",
    "quantity": 2,
    "unit_price": 40000,
    }

@pytest.mark.asyncio
async def test_create_invoice(client):
    token = await create_employee_and_get_token(client) 

    response = await client.post(
        "/invoices/",
        json=invoice_payload(),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["invoice_number"] == "IN_001"
    assert response_data["customer_email"] == "customer@gmail.com"