from fastapi import Depends

from app.common.utils import get_language
from app.model.repository.company import CompanyRepository
from app.model.repository.tag import TagRepository


class BaseService:
    def __init__(
        self,
        lang: str = Depends(get_language),
        company: CompanyRepository = Depends(CompanyRepository),
        tag: TagRepository = Depends(TagRepository)
    ):
        self._lang = lang
        self._company = company
        self._tag = tag
