from fastapi import APIRouter, Depends

from app.common.schemas import CompanyCreateInfo, TagCreateInfo
from app.service.company import CompanyService
from app.service.tag import TagService

router = APIRouter()


@router.get("/companies/{company_name}")
async def search_company(
    company_name: str,
    service: CompanyService = Depends(CompanyService),
) -> dict:
    """회사 이름으로 회사 검색"""
    return await service.search_by_name(company_name)


@router.post("/companies")
async def create_company(
    body: CompanyCreateInfo,
    service: CompanyService = Depends(CompanyService),
) -> dict:
    """새로운 회사 추가"""
    return await service.create(body)


@router.get("/tags")
async def search_tag(
    query: str,
    service: TagService = Depends(TagService),
) -> list:
    """태그명으로 회사 검색"""
    return await service.search_by_name(query)


@router.put("/companies/{company_name}/tags")
async def add_company_tag(
    company_name: str,
    body: list[TagCreateInfo],
    service: TagService = Depends(TagService),
) -> dict:
    """회사 태그 정보 추가"""
    return await service.add_to_company(company_name, body)


@router.delete("/companies/{company_name}/tags/{tag_name}")
async def delete_company_tag(
    company_name: str,
    tag_name: str,
    service: TagService = Depends(TagService),
) -> dict:
    """회사 태그 정보 삭제"""
    return await service.remove(company_name, tag_name)
