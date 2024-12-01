from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.connection import db


class BaseRepository:
    def __init__(self, session: AsyncSession = Depends(db.session)):
        self._session = session

    def add_all(self, instance):
        self._session.add_all(instance)
