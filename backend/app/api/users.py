from http.client import HTTPException

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from .. import schemas
from ..core import deps
from ..database import models, crud

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.UserResponse)
def read_self(user: models.User = Depends(deps.get_current_user)):
    return user


@router.get("/all", response_model=list[schemas.UserResponse])
def read_all_users(*,
                   db: Session = Depends(deps.get_db),
                   admin: models.User = Depends(deps.get_admin_user)):
    return crud.get_all_users(db)


@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate,
                *,
                db: Session = Depends(deps.get_db),
                admin: models.User = Depends(deps.get_admin_user),
                config: models.AppConfig = Depends(deps.get_config)):
    try:
        return crud.create_user(db, user,
                                password_expire_days=config.password_expire_days)

    except IntegrityError:
        raise HTTPException(status_code=400, detail="Użytkownik o podanej nazwie już istnieje")


@router.patch("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int,
                user: schemas.UserUpdate,
                *,
                db: Session = Depends(deps.get_db),
                admin: models.User = Depends(deps.get_admin_user)):
    db_user = crud.get_user_by_id(db, user_id)
    return crud.update_user(db, db_user, user, force_password_change=True)


@router.delete("/{user_id}")
def delete_user(user_id: int,
                *,
                db: Session = Depends(deps.get_db),
                admin: models.User = Depends(deps.get_admin_user)):
    db_user = crud.get_user_by_id(db, user_id)
    crud.delete_user(db, db_user)
    return {"message": "User deleted"}
