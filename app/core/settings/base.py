from pydantic_settings import BaseSettings as _BaseSettings


class BaseSettings(_BaseSettings):
    """Base Settings"""

    APP_ENV: str
    DEBUG: str

    SECRET_KEY: str

    TIMEZONE: str = "Asia/Seoul"

    DB_URL: str
    SQLALCHEMY_POOL_SIZE: int = 10
