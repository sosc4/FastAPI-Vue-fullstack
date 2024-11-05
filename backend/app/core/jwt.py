import jwt
from fastapi import HTTPException

from .settings import settings

ALGORITHM = "HS256"


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token nieprawidłowy")
