from .base import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "test"
    DEBUG: bool = False

    SECRET_KEY: str = "test"

    DB_URL: str = "postgresql+asyncpg://testuser:password@127.0.0.1:5432/testdb"
