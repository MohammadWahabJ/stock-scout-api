from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Any
from .config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# JWT secret key and algorithm
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.APP_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> Any:
    credentials_exception = Exception("Could not validate credentials")
    try:
        payload = jwt.decode(token, settings.APP_SECRET,
                             algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception
