from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # secrets

    # .env
    PROXY_USR: str
    PROXY_PWD: str
    PROXY_IP: str
    PROXY_PORT: int = Field(None, ge=1)

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        # secrets_dir='keys',
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
