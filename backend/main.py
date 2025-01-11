from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session

from app.api import router
from app.core.settings import settings
from app.database import crud
from app.database.database import engine
from app.schemas import UserCreate


def init():
    SQLModel.metadata.create_all(engine)
    db = Session(engine)

    if crud.get_user_by_username(db, settings.ADMIN_USERNAME):
        return

    user = crud.create_user(db, UserCreate(
        username=settings.ADMIN_USERNAME,
        password=settings.ADMIN_INIT_PASSWORD,
    ), is_admin=True, admin_id=1)

    crud.create_config(db, user.id)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
