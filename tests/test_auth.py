def test_register_student(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Phil",
            "email": "phil@test.com",
            "password": "password123",
            "role": "student",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "phil@test.com"
    assert data["role"] == "student"
    assert "hashed_password" not in data


def test_register_duplicate_email_fails(client):
    payload = {
        "name": "Phil",
        "email": "dup@test.com",
        "password": "password123",
        "role": "student",
    }
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400


def test_login_returns_token(client):
    client.post(
        "/auth/register",
        json={
            "name": "Phil",
            "email": "login@test.com",
            "password": "password123",
            "role": "student",
        },
    )
    response = client.post(
        "/auth/login",
        data={"username": "login@test.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password_fails(client):
    client.post(
        "/auth/register",
        json={
            "name": "Phil",
            "email": "wrong@test.com",
            "password": "password123",
            "role": "student",
        },
    )
    response = client.post(
        "/auth/login",
        data={"username": "wrong@test.com", "password": "wrongpass"},
    )
    assert response.status_code == 401


def test_me_endpoint_requires_auth(client):
    response = client.get("/users/me")
    assert response.status_code == 401


def test_me_endpoint_returns_user(client, student_token):
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "student@test.com"


def test_register_cannot_create_admin(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Sneaky",
            "email": "sneaky@test.com",
            "password": "password123",
            "role": "admin",
        },
    )
    assert response.status_code == 201
    assert response.json()["role"] == "student"
