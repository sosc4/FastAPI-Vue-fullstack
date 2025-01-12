import time
from datetime import datetime, UTC

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from .jwt import decode_access_token
from ..database import crud
from ..database.database import engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    with Session(engine) as session:
        yield session


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="„Login lub hasło niepoprawne",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        session_expires_at: int = payload.get("exp")
        if time.time() >= session_expires_at:
            raise HTTPException(status_code=400, detail="Sesja wygasła")

    except jwt.PyJWTError:
        raise credentials_exception

    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(user=Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Użytownik nieaktywny")

    if user.force_password_change:
        raise HTTPException(status_code=400, detail="Wymagana zmiana hasła")

    if user.password_expires and datetime.now(UTC) >= user.password_expires:
        raise HTTPException(status_code=400, detail="Hasło wygasło")

    return user


def get_admin_user(user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=400, detail="Użytkownik nie jest administratorem")

    return user


def get_config(db: Session = Depends(get_db)):
    return crud.get_config(db)
