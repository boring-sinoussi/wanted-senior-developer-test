from .base import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "local"
    DEBUG: bool = True
