from functools import lru_cache
from importlib import import_module
import os
from pathlib import Path

from .base import BaseSettings


BASE_DIR = Path(__file__).parents[3]


@lru_cache()
def get_settings() -> BaseSettings:
    env = os.getenv("APP_ENV", "local")
    print(f"Load Settings: {env}")
    settings = import_module(f".{env}", "app.core.settings")
    return settings.Settings(
        _env_file=(
            BASE_DIR / f".env.{env}",
            BASE_DIR / ".env",
        ),
    )
