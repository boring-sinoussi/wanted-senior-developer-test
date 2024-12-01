from pydantic import BaseModel


LanguageName = dict[str, str]


class TagCreateInfo(BaseModel):
    tag_name: LanguageName


class CompanyCreateInfo(BaseModel):
    company_name: LanguageName
    tags: list[TagCreateInfo]
