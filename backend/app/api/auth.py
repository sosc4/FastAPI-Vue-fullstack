import time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlmodel import Session

from .. import schemas, enums
from ..core import deps
from ..core.jwt import create_access_token
from ..core.password import validate_password
from ..core.security import verify_password, validate_otp
from ..database import crud
from ..database import models

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=schemas.JWTAccessToken)
def login(
        username: str = Form(...),
        password: str = Form(...),
        *,
        a: Optional[int] = Form(None),
        x: Optional[int] = Form(None),
        config: models.AppConfig = Depends(deps.get_config),
        db: Session = Depends(deps.get_db)
):
    if any(param is not None for param in (a, x)) and not all(param is not None for param in (a, x)):
        raise HTTPException(
            status_code=400,
            detail="Haso jednorazowe niepoprawne"
        )

    db_user = crud.get_user_by_username(db, username=username)

    state = enums.LogStatus.SUCCESS
    message = None

    try:
        attempts = crud.read_recent_failed_logins(db, db_user.id)
        if len(attempts) > config.login_attempts:
            raise HTTPException(status_code=400, detail="Konto zablokowane z powodu zbyt wielu prób logowania")

        password_passed = verify_password(password, db_user.hashed_password)
        otp_passed = validate_otp(password, x, a) and db_user.enable_otp

        if not db_user or not (password_passed or otp_passed):
            raise HTTPException(status_code=400, detail="Login lub hasło niepoprawne")

        return {
            "access_token": create_access_token(data={"sub": db_user.username,
                                                      "exp": int(time.time()) + config.session_expire_seconds}),
            "token_type": "bearer"
        }

    except Exception as e:
        state = enums.LogStatus.FAILURE
        message = str(e)
        raise e

    finally:
        crud.create_log(db, db_user.id, enums.LogEvent.LOGIN, state)


@router.post("/refresh", response_model=schemas.JWTAccessToken)
def refresh_token(
        db: Session = Depends(deps.get_db),
        user=Depends(deps.get_current_user),
        config: models.AppConfig = Depends(deps.get_config)):
    return {
        "access_token": create_access_token(data={"sub": user.username,
                                                  "exp": int(time.time()) + config.session_expire_seconds}),
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


@router.post("/logout")
def logout(
        db: Session = Depends(deps.get_db),
        user=Depends(deps.get_current_user)):
    crud.create_log(db, user.id, enums.LogEvent.LOGOUT, enums.LogStatus.SUCCESS)
    return {"message": "Logout successful"}
