import asyncio
import csv

from httpx import ASGITransport, AsyncClient
import pytest
import pytest_asyncio
from sqlalchemy import insert

from app.asgi import app
from app.core.connection import db
from app.model.base import Base
from app.model.company import (
    Company,
    CompanyTag,
    CompanyLanguage,
    Tag,
    TagLanguage,
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def setup_db():
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def setup_data(setup_db):
    with open("./company_tag_sample.csv") as f:
        rdr = csv.reader(f)
        next(rdr)
        companies = []
        for idx, line in enumerate(rdr):
            company_lang = [
                {"language": lang, "name": line[i]} for i, lang in enumerate(["ko", "en", "jp"]) if line[i]
            ]
            companies.append(
                {"company": Company(), "company_lang": company_lang, "tag": [int(i[3:]) for i in line[3].split("|")]}
            )

    async with db._session() as session:
        try:
            # 태그 생성
            session.add_all([Tag() for _ in range(30)])
            await session.commit()
            session.add_all(
                [
                    TagLanguage(tag_id=i, language=lang, name=f"{name}_{i}")
                    for i in range(1, 31)
                    for lang, name in [("ko", "태그"), ("en", "tag"), ("jp", "タグ")]
                ]
            )

            # 회사 생성
            session.add_all([comp["company"] for comp in companies])
            await session.flush()
            session.add_all(
                [CompanyLanguage(company_id=comp["company"].id, **dl) for comp in companies for dl in comp["company_lang"]]
            )
            await session.commit()

            # 회사 & 태그 연결
            await session.execute(
                insert(CompanyTag).values(
                    [{"company_id": d["company"].id, "tag_id": tag_id} for d in companies for tag_id in d["tag"]]
                )
            )
            await session.commit()
        finally:
            await session.close()


@pytest_asyncio.fixture
async def api(setup_data):
    async with AsyncClient(
        base_url="http://test.com", transport=ASGITransport(app)
    ) as client:
        yield client
