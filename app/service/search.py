from fastapi.exceptions import HTTPException

from .base import BaseService


class SearchCompanyService(BaseService):
    async def autocomplete(self, text) -> list:
        company = await self._company.find_contains_name(text, self._lang)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return [{"company_name": comp.company_name} for comp in company]
