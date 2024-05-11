from pathlib import Path
from typing import Literal, Tuple, Type

from pydantic import PositiveInt
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

type LogLevelsAllowed = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class DBSetiings(BaseSettings):
    # DB settings
    SQLITE_DB_FILE: Path | None = None

    @property
    def DATABASE_URL(self) -> str:
        if self.SQLITE_DB_FILE:
            return f"sqlite+aiosqlite:///{self.SQLITE_DB_FILE}"
        raise ValueError("DB URL is undefined")


class Settings(DBSetiings):
    # secrets

    # .env
    # general settings
    LOG_LEVEL: LogLevelsAllowed = "DEBUG"
    LOG_TO_FILE: bool = False
    LOG_FILE: Path = Path("logs/llmassist.log")
    LOG_FILE_LEVEL: LogLevelsAllowed = "DEBUG"

    # proxy settings
    # tor
    TOR_SOCKS5_PORT: PositiveInt | None = None

    # tgbot settings
    TGBOT_TOKEN: str | None = None

    # DEBUG mode
    DEBUG: bool = False

    # read only .env and secrets
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        # here we choose to ignore arguments from init_settings
        return dotenv_settings, file_secret_settings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        # secrets_dir='keys',
    )
