from fastapi import APIRouter

from .company import router as company_router
from .home import router as home_router
from .search import router as search_router

router = APIRouter()
router.include_router(company_router)
router.include_router(home_router)
router.include_router(search_router)
