from fastapi import APIRouter

from . import statistics
from . import parsing
from . import analytics
from . import users

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(statistics.router, prefix="/statistics")
main_router.include_router(parsing.router, prefix="/parsing")
main_router.include_router(users.router, prefix="/users")