from fastapi import APIRouter, Depends

from app.service.search import SearchCompanyService

router = APIRouter()


@router.get("/search")
async def autocomplete(
    query: str,
    service: SearchCompanyService = Depends(SearchCompanyService)
) -> list:
    """회사명 자동완성"""
    return await service.autocomplete(query)
