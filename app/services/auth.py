from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repository import user as user_repo
from app.schemas.user import UserCreate
from app.security import create_access_token, hash_password, verify_password


def register_user(db: Session, payload: UserCreate) -> User:
    if user_repo.get_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )
    return user_repo.create(
        db,
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="student",
    )


def create_admin_user(
    db: Session, name: str, email: str, password: str
) -> User | None:
    if user_repo.get_by_email(db, email):
        return None
    return user_repo.create(
        db,
        name=name,
        email=email,
        hashed_password=hash_password(password),
        role="admin",
    )


def authenticate_user(db: Session, email: str, password: str) -> str:
    user = user_repo.get_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return create_access_token(subject=user.id)
