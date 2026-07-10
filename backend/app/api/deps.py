"""
Reusable FastAPI dependencies shared across routers.
"""
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.user import User
from app.exceptions.custom_exceptions import NotAuthenticatedError

# tokenUrl points at the OAuth2 password login endpoint used by OpenAPI docs.
# The frontend still uses the JSON /login route directly.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    if not token:
        raise NotAuthenticatedError()

    email = decode_access_token(token)
    if not email:
        raise NotAuthenticatedError()

    user = (
        db.query(User)
        .options(joinedload(User.role))
        .filter(User.email == email)
        .first()
    )
    if not user:
        raise NotAuthenticatedError()

    return user
