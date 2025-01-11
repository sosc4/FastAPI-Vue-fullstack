from fastapi import APIRouter, Depends, HTTPException, Form
from sqlmodel import Session

from .. import schemas
from ..core import deps
from ..core.jwt import create_access_token
from ..core.password import validate_password
from ..core.security import verify_password
from ..database import crud
from ..database import models

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=schemas.JWTAccessToken)
def login(username: str = Form(...),
          password: str = Form(...),
          *,
          db: Session = Depends(deps.get_db)):
    db_user = crud.get_user_by_username(db, username=username)
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Login lub hasło niepoprawne")

    return {
        "access_token": create_access_token(data={"sub": db_user.username}),
        "token_type": "bearer"
    }


@router.patch("/password", response_model=schemas.UserResponse)
def change_password(password: schemas.PasswordChange,
                    *,
                    db: Session = Depends(deps.get_db),
                    user=Depends(deps.get_current_user),
                    config: models.AppConfig = Depends(deps.get_config)
                    ):
    if config.password_validation_enabled:
        validate_password(password.new_password,
                          config.password_min_length,
                          config.password_require_digit,
                          config.password_require_special)

    if not verify_password(password.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Hasło niepoprawne")

    user = crud.change_password(db, user, password.new_password,
                                password_expire_days=config.password_expire_days,
                                admin_id=user.id)
    return user
