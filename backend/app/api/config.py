from fastapi import APIRouter, Depends
from sqlmodel import Session

from .. import schemas
from ..core import deps
from ..database import crud

router = APIRouter(prefix="/config", tags=["app config"])


@router.get("/")
def get_config(
        db: Session = Depends(deps.get_db),
        user=Depends(deps.get_current_user),
):
    config = crud.get_config(db)
    return config


@router.patch("/")
def update_config(
        config: schemas.AppConfigUpdate,
        db: Session = Depends(deps.get_db),
        user=Depends(deps.get_admin_user),
):
    return crud.update_config(db, config)


@router.post("/password/validation")
def toggle_password_validation(
        db: Session = Depends(deps.get_db),
        user=Depends(deps.get_admin_user),
):
    config = crud.toggle_password_validation(db)
    return config
