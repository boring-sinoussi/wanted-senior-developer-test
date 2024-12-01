from fastapi.exceptions import HTTPException

from app.common.schemas import TagCreateInfo
from .base import BaseService


class TagService(BaseService):
    @staticmethod
    def _normalize_company_name(data) -> str:
        if name := getattr(data, "company_name", None):
            return name
        languages = data.Company.languages
        return languages[0].name

    async def search_by_name(self, tag_name: str) -> list:
        if not (companies := await self._company.find_by_tag_name(tag_name, self._lang)):
            raise HTTPException(status_code=404, detail="Company not found")
        return [
            {"company_name": self._normalize_company_name(row)}
            for row in companies
        ]

    async def add_to_company(self, company_name: str, tags: list[TagCreateInfo]):
        company = await self._company.find_by_name(company_name, self._lang)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        for tag_info in tags:
            tag_name = tag_info.tag_name[self._lang]
            if not (tag := await self._tag.find_by_name(tag_name)):
                tag = await self._tag.create(tag_info.tag_name)
            elif await self._tag.exists(tag.id, company[0].Company.id):
                continue
            await self._tag.link(company[0].Company.id, tag.id)

        return {
            "company_name": company[0].company_name,
            "tags": [
                tag.name
                for tag
                in await self._tag.find_company_tags(
                    company[0].Company.id, self._lang
                )
            ],
        }

    async def remove(self, company_name, tag_name: str):
        company = await self._company.find_by_name(company_name, self._lang)
        tag = await self._tag.find_by_name(tag_name)
        await self._tag.unlink(company[0].Company.id, tag.id)
        return {
            "company_name": company[0].company_name,
            "tags": [
                tag.name
                for tag
                in await self._tag.find_company_tags(
                    company[0].Company.id, self._lang
                )
            ],
        }
