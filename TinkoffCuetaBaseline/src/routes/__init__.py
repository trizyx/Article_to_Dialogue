from fastapi import APIRouter

from .ping import router as ping_router
from .api import router as api_router

routers = [
    ping_router,
    api_router,
]

api_routers = APIRouter()

for r in routers:
    api_routers.include_router(r)
