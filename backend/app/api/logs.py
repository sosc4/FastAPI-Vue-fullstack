from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..core import deps
from ..database import crud

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("/")
def read_logs(db: Session = Depends(deps.get_db),
              user=Depends(deps.get_admin_user)):
    return crud.read_logs(db)
