from .base import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "production"
    DEBUG: bool = False
