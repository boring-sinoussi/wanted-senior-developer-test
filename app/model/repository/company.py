from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.common.schemas import LanguageName
from app.model.company import Company, CompanyLanguage, CompanyTag, TagLanguage
from .base import BaseRepository


class CompanyRepository(BaseRepository):
    async def find_contains_name(self, text: str, language: str):
        result = await self._session.execute(
            select(
                Company,
                (
                    select(CompanyLanguage.name)
                    .where(
                        CompanyLanguage.language == language,
                        Company.id == CompanyLanguage.company_id,
                    )
                    .scalar_subquery()
                    .label("company_name")
                ),
            )
            .where(
                Company.id.in_(
                    select(CompanyLanguage.company_id)
                    .where(CompanyLanguage.name.like(f"%{text}%"))
                ),
            )
            .order_by(Company.id)
        )
        return result.all()

    async def find_by_name(self, company_name: str, language: str):
        result = await self._session.execute(
            select(
                Company,
                (
                    select(CompanyLanguage.name)
                    .where(
                        CompanyLanguage.language == language,
                        Company.id == CompanyLanguage.company_id,
                    )
                    .scalar_subquery()
                    .label("company_name")
                ),
            )
            .where(
                Company.id.in_(
                    select(CompanyLanguage.company_id)
                    .where(CompanyLanguage.name == company_name)
                ),
            )
        )
        return result.all()

    async def find_by_tag_name(self, tag_name: str, language: str):
        result = await self._session.execute(
            select(
                Company,
                (
                    select(CompanyLanguage.name)
                    .where(
                        CompanyLanguage.language == language,
                        Company.id == CompanyLanguage.company_id,
                    )
                    .scalar_subquery()
                    .label("company_name")
                ),
            )
            .where(
                Company.id.in_(
                    select(CompanyTag.company_id)
                    .join(TagLanguage, CompanyTag.tag_id == TagLanguage.tag_id)
                    .where(TagLanguage.name == tag_name)
                ),
            )
            .order_by(Company.id)
            .options(selectinload(Company.languages))
        )
        return result.all()

    async def create(self, company_names: LanguageName) -> Company:
        company = Company()
        self._session.add(company)
        await self._session.flush()
        self._session.add_all(
            CompanyLanguage(company_id=company.id, language=lang, name=name)
            for lang, name in company_names.items()
        )
        await self._session.commit()
        return company
