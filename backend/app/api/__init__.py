from fastapi import APIRouter

from .auth import router as auth_router
from .config import router as config_router
from .logs import router as logs_router
from .users import router as users_router

router = APIRouter()

routes = [
    auth_router,
    users_router,
    config_router,
    logs_router,
]
for route in routes:
    router.include_router(route)

__all__ = ["router"]
