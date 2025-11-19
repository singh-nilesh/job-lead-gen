""" Integration tests for authentication API endpoints."""
from fastapi.testclient import TestClient
from app.core.config import Settings
from app.db.sqlalchemyConfig import teardown_db
from app.models import User
from app.main import app
import pytest

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c
    teardown_db()

new_usser = User(
    name="Test User",
    email="testuser@example.com",
    phone="+223456789012345",
    location="Test Location",
    password="TestPass123"
)


def test_register(client):
    """ Test user registration endpoint """
    response = client.post(
        "auth/register",
        json=new_usser.model_dump()
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == new_usser.email
    assert data["id"] == 1, ''' First user should have ID 1'''

    # Attempt to register the same user again
    response_dup = client.post(
        "/auth/register",
        json=new_usser.model_dump()
    )
    assert response_dup.status_code == 400, "Duplicate registration should fail"


def test_login(client):
    """ Test user login endpoint """
    # First, register the user
    res = client.post(
        "/auth/register",
        json=new_usser.model_dump()
    )
    assert res.status_code == 200, "Register User before Login"

    # Now, attempt to login
    response = client.post(
        "/auth/login",
        data={
            "username": new_usser.email,
            "password": new_usser.password
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
