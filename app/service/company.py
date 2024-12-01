from fastapi.exceptions import HTTPException

from app.common.schemas import CompanyCreateInfo
from app.model.company import TagLanguage
from .base import BaseService


class CompanyService(BaseService):
    async def search_by_name(self, company_name) -> dict:
        company = await self._company.find_by_name(company_name, self._lang)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return {
            "company_name": company[0].company_name,
            "tags": [
                tag.name
                for tag in await self._tag.find_company_tags(
                    company[0].Company.id, self._lang
                )
            ],
        }

    async def create(self, company_info: CompanyCreateInfo):
        company = await self._company.create(company_info.company_name)
        for tag_info in company_info.tags:
            if tags := await self._tag.find_by_languages_and_name(tag_info.tag_name):
                current_language = {row.TagLanguage.language for row in tags}
                tag_id = tags[0].TagLanguage.tag_id
                # 존재하지 않는 언어는 추가로 입력
                if target := {k for k in tag_info.tag_name.keys()} - current_language:
                    self._tag.add_all(
                        [
                            TagLanguage(
                                tag_id=tag_id,
                                language=lang,
                                name=tag_info.tag_name[lang]
                            )
                            for lang in target
                        ]
                    )
            else:
                # 신규 태그 생성
                tag = await self._tag.create(tag_info.tag_name)
                tag_id = tag.id
            await self._tag.link(company.id, tag_id)
        return {
            "company_name": company_info.company_name.get(self._lang),
            "tags": [
                tag.name
                for tag in await self._tag.find_company_tags(
                    company.id, self._lang
                )
            ],
        }
