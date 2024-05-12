import os
from datetime import timedelta, datetime, timezone

from jose import jwt
from passlib.context import CryptContext

ACCESS_TOKEN_EXPIRE_MINUTES = 60  # default expiry time
ALGORITHM = "HS256"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """
        Hash password with bcrypt
    """
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    """
        Verify hashed password
    """
    return password_context.verify(password, hashed_pass)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
        Create JWT access token
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"email": str(data["email"]), "user_id": str(data["user_id"]), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, os.environ["JWT_SECRET_KEY"], algorithm=ALGORITHM)

    return encoded_jwt
