import os

os.environ.setdefault("JWT_SECRET", "test-secret-key-for-pytest-only")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.services.auth import create_admin_user

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_token(client):
    db = TestingSessionLocal()
    try:
        create_admin_user(
            db,
            name="Admin",
            email="admin@test.com",
            password="password123",
        )
    finally:
        db.close()

    response = client.post(
        "/auth/login",
        data={"username": "admin@test.com", "password": "password123"},
    )
    return response.json()["access_token"]


@pytest.fixture
def student_token(client):
    client.post(
        "/auth/register",
        json={
            "name": "Student",
            "email": "student@test.com",
            "password": "password123",
        },
    )
    response = client.post(
        "/auth/login",
        data={"username": "student@test.com", "password": "password123"},
    )
    return response.json()["access_token"]
