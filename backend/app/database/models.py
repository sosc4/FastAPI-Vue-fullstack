import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=True)
    force_password_change: bool = Field(default=True)
    password_expires: Optional[datetime.datetime] = Field(default=None)
    last_password_change: datetime.datetime = Field(default=datetime.datetime.now(datetime.timezone.utc))
    old_passwords: str = Field("")


class AppConfig(SQLModel, table=True):
    id: int = Field(primary_key=True)
    password_validation_enabled: bool = Field(default=True)
    password_min_length: int = Field(default=12)
    password_require_digit: bool = Field(default=True)
    password_require_special: bool = Field(default=True)
    password_expire_days: int = Field(default=30)


__all__ = ["User", "AppConfig"]
