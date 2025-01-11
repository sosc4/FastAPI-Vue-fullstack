import datetime
from typing import Optional

from fastapi import HTTPException
from passlib import exc
from sqlmodel import Session, select

from . import models
from .. import schemas, enums
from ..core import security


def create_log(db: Session,
               user_id: int,
               event: enums.LogEvent,
               status: enums.LogStatus,
               *,
               message: Optional[str] = None) -> models.Log:
    log = models.Log(user_id=user_id, event=event, status=status, message=message)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_user_by_username(db: Session, username: str) -> models.User:
    result = db.exec(select(models.User).where(models.User.username == username))
    return result.first()


def create_user(db: Session,
                user: schemas.UserCreate,
                *,
                is_admin: bool = False,
                password_expire_days: int = 30) -> models.User:
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(username=user.username,
                          hashed_password=hashed_password,
                          is_admin=is_admin,
                          old_passwords=f"{hashed_password} ",
                          password_expires=datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=30)
                          )

    status = enums.LogStatus.SUCCESS
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except Exception as e:
        status = enums.LogStatus.FAILURE
        raise e

    finally:
        create_log(db, db_user.id, enums.LogEvent.USER_ADDED, status)


def change_password(db: Session,
                    user: models.User,
                    new_password: str,
                    *,
                    force_change: bool = False,
                    password_expire_days: int = 30
                    ) -> models.User:
    status = enums.LogStatus.SUCCESS

    try:
        old_passwords = user.old_passwords.split(" ")
        for x in old_passwords:
            try:
                if security.verify_password(new_password, x):
                    raise HTTPException(status_code=400, detail="Hasło już było użyte")

            except exc.UnknownHashError:
                continue

        user.hashed_password = security.get_password_hash(new_password)
        user.old_passwords = " ".join([user.hashed_password, *old_passwords])

        user.last_password_change = datetime.datetime.now(datetime.UTC)
        user.force_password_change = force_change

        user.password_expires = user.last_password_change + datetime.timedelta(days=password_expire_days)

        db.commit()
        db.refresh(user)
        return user

    except Exception as e:
        status = enums.LogStatus.FAILURE
        raise e

    finally:
        create_log(db, user.id, enums.LogEvent.PASSWORD_CHANGE, status)


def get_all_users(db: Session) -> list[models.User]:
    return db.exec(select(models.User)).all()


def update_user(db: Session,
                db_user: models.User,
                user: schemas.UserUpdate,
                *,
                force_password_change: bool = False
                ) -> models.User:
    status = enums.LogStatus.SUCCESS

    try:
        for field, value in user.model_dump(exclude_none=True).items():
            if field == "password":
                db_user = change_password(db, db_user, value,
                                          force_change=force_password_change
                                          )
                continue

            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)
        return db_user

    except Exception as e:
        status = enums.LogStatus.FAILURE
        raise e

    finally:
        create_log(db, db_user.id, enums.LogEvent.USER_UPDATED, status)


def update_config(db: Session, config: schemas.AppConfigUpdate) -> models.AppConfig:
    status = enums.LogStatus.SUCCESS

    try:
        db_config = get_config(db)
        for field, value in config.model_dump(exclude_none=True).items():
            setattr(db_config, field, value)

        db.commit()
        db.refresh(db_config)
        return db_config

    except Exception as e:
        status = enums.LogStatus.FAILURE
        raise e

    finally:
        create_log(db, 0, enums.LogEvent.CONFIG_UPDATED, status)


def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.get(models.User, user_id)


def delete_user(db: Session, db_user: models.User):
    success = enums.LogStatus.SUCCESS

    try:
        db.delete(db_user)
        db.commit()

    except Exception as e:
        success = enums.LogStatus.FAILURE
        raise e

    finally:
        create_log(db, db_user.id, enums.LogEvent.USER_DELETED, success)


def toggle_password_validation(db: Session, user_id: int):
    status = enums.LogStatus.SUCCESS

    try:
        config = db.exec(select(models.AppConfig)).first()
        config.password_validation_enabled = not config.password_validation_enabled
        db.commit()
        db.refresh(config)
        return config

    except Exception as e:
        status = enums.LogStatus.FAILURE
        raise e

    finally:
        create_log(db, user_id, enums.LogEvent.CONFIG_UPDATED, status,
                   message="Password validation enabled" if status == enums.LogStatus.SUCCESS
                   else "Password validation disabled")


def get_config(db: Session):
    return db.exec(select(models.AppConfig)).first()


def create_config(db: Session, user_id: int):
    status = enums.LogStatus.SUCCESS

    try:
        config = models.AppConfig()
        db.add(config)
        db.commit()
        db.refresh(config)
        return config

    except Exception as e:
        status = enums.LogStatus.FAILURE
        raise e

    finally:
        create_log(db, user_id, enums.LogEvent.CONFIG_UPDATED, status)
