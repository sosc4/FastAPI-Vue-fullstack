from datetime import datetime, UTC
from typing import Optional

from pydantic import BaseModel, model_validator


class UserCreate(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None
    password_expires: Optional[datetime] = None


class UserResponse(BaseModel):
    id: int
    username: str
    is_admin: bool
    is_active: bool
    force_password_change: bool
    password_expires: Optional[datetime]

    @model_validator(mode="before")
    def set_force_password_change(cls, user):
        if user.password_expires:
            if user.password_expires.tzinfo is None:
                user.password_expires = user.password_expires.replace(tzinfo=UTC)

            if datetime.now(UTC) >= user.password_expires:
                user.force_password_change = True

        return user

    class Config:
        from_attributes = True


class JWTAccessToken(BaseModel):
    access_token: str
    token_type: str


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class AppConfig(BaseModel):
    password_validation_enabled: bool
    password_min_length: int
    password_require_digit: bool
    password_require_special: bool
    password_expire_days: int
    login_attempts: int
    session_expire_seconds: int


class AppConfigUpdate(AppConfig):
    password_validation_enabled: Optional[bool] = None
    password_min_length: Optional[int] = None
    password_require_digit: Optional[bool] = None
    password_require_special: Optional[bool] = None
    password_expire_days: Optional[int] = None
    login_attempts: Optional[int] = None
    session_expire_seconds: Optional[int] = None


__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "JWTAccessToken",
    "PasswordChange",
    "AppConfig",
    "AppConfigUpdate"
]
