import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_signup_and_login():
    import uuid
    email = f"testuser_{uuid.uuid4()}@example.com"
    password = "testpassword"

    # Signup
    response = client.post("/auth/signup", json={"email": email, "password": password})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == email

    # Duplicate signup should fail
    response = client.post("/auth/signup", json={"email": email, "password": password})
    assert response.status_code == 400

    # Login
    response = client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Login with wrong password should fail
    response = client.post("/auth/login", json={"email": email, "password": "wrongpass"})
    assert response.status_code == 401 