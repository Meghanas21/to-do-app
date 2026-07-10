"""
Business logic for registration/login. Kept separate from the router so the
router only deals with HTTP concerns (status codes, request/response shape)
and this file only deals with the actual auth rules.
"""
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.role import Role
from app.models.user import User
from app.schemas.user import UserCreate
from app.exceptions.custom_exceptions import (
    DuplicateEmailError,
    InvalidCredentialsError,
)


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def register_user(db: Session, user_in: UserCreate) -> User:
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise DuplicateEmailError(user_in.email)

    default_role = db.query(Role).filter(Role.name == "user").first()
    if not default_role:
        default_role = Role(name="user")
        db.add(default_role)
        db.commit()
        db.refresh(default_role)

    user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role_id=default_role.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise InvalidCredentialsError()
    return user


def create_token_for_user(user: User) -> str:
    return create_access_token(subject=user.email)
