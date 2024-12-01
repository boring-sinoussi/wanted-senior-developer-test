from sqlalchemy import ScalarResult, and_, delete, literal, or_, select

from app.common.schemas import LanguageName
from app.model.company import CompanyTag, Tag, TagLanguage
from .base import BaseRepository


class TagRepository(BaseRepository):
    async def find_company_tags(
        self, company_id: int, language: str
    ) -> ScalarResult:
        result = await self._session.execute(
            select(TagLanguage)
            .join(CompanyTag, TagLanguage.tag_id == CompanyTag.tag_id)
            .where(
                CompanyTag.company_id == company_id,
                TagLanguage.language == language,
            )
        )
        return result.scalars()

    async def find_by_name(self, tag_name: str) -> Tag:
        result = await self._session.execute(
            select(Tag)
            .where(
                Tag.id.in_(
                    select(TagLanguage.tag_id)
                    .where(TagLanguage.name == tag_name)
                )
            )
        )
        return result.scalar_one_or_none()

    async def find_by_languages_and_name(self, tag_name: LanguageName):
        result = await self._session.execute(
            select(TagLanguage)
            .where(
                or_(
                    and_(
                        TagLanguage.name == name,
                        TagLanguage.language == lang,
                    )
                    for lang, name in tag_name.items()
                )
            )
        )
        return result.all()

    async def exists(self, tag_id: int, company_id: int):
        result = await self._session.execute(
            select(literal(1))
            .where(
                CompanyTag.company_id == company_id,
                CompanyTag.tag_id == tag_id,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, tag_names: LanguageName):
        tag = Tag()
        self._session.add(tag)
        await self._session.flush()
        self._session.add_all(
            TagLanguage(tag_id=tag.id, language=lang, name=name)
            for lang, name in tag_names.items()
        )
        await self._session.commit()
        return tag

    async def link(self, company_id: int, tag_id: int):
        self._session.add(CompanyTag(company_id=company_id, tag_id=tag_id))
        await self._session.commit()

    async def unlink(self, company_id: int, tag_id: int):
        await self._session.execute(
            delete(CompanyTag)
            .where(
                CompanyTag.company_id == company_id,
                CompanyTag.tag_id == tag_id,
            )
        )
