from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .base import BaseModel


class Company(BaseModel):
    """회사 메타 정보"""

    __tablename__ = "tb_company"

    id = Column(BigInteger, primary_key=True)
    is_active = Column(Boolean, comment="활성화 여부", nullable=False, default=True)
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )
    languages = relationship("CompanyLanguage", back_populates="company")


class CompanyLanguage(BaseModel):
    """언어별 회사 정보"""

    __tablename__ = "tb_company_lang"
    __table_args__ = (UniqueConstraint("name", "language"),)

    id = Column(BigInteger, primary_key=True)
    company_id = Column(
        BigInteger, ForeignKey("tb_company.id", ondelete="CASCADE")
    )
    language = Column(String(5), comment="언어 구분", nullable=True)
    name = Column(String(50), comment="회사명", nullable=True)
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )
    company = relationship("Company", back_populates="languages")


class Tag(BaseModel):
    """태그 메타 정보"""

    __tablename__ = "tb_tag"

    id = Column(BigInteger, primary_key=True)
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )


class TagLanguage(BaseModel):
    """언어별 태그 정보"""

    __tablename__ = "tb_tag_lang"
    __table_args__ = (UniqueConstraint("name", "language"),)

    id = Column(BigInteger, primary_key=True)
    tag_id = Column(
        BigInteger, ForeignKey("tb_tag.id", ondelete="CASCADE")
    )
    language = Column(String(5), comment="언어 구분", nullable=True)
    name = Column(String(50), comment="회사명", nullable=True)
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )


class CompanyTag(BaseModel):
    """회사 & 태그 매핑 정보"""

    __tablename__ = "tb_company_tag"
    __table_args__ = (UniqueConstraint("company_id", "tag_id"),)

    id = Column(BigInteger, primary_key=True)
    company_id = Column(
        BigInteger, ForeignKey("tb_company.id", ondelete="CASCADE")
    )
    tag_id = Column(
        BigInteger, ForeignKey("tb_tag.id", ondelete="CASCADE")
    )
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )
