from pathlib import Path
from typing import Literal, Tuple, Type

from pydantic import PositiveInt, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

type LogLevelsAllowed = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        # ignore empty variables and use default instead
        # env_ignore_empty=True,
        extra="ignore",
        # secrets_dir='keys',
    )


class DBSetiings(EnvBaseSettings):
    # DB settings
    # sqlite file could be "" for in memory DB
    SQLITE_DB_FILE: str | None = None

    @property
    def DATABASE_URL(self) -> str:
        if self.SQLITE_DB_FILE is not None:
            return f"sqlite+aiosqlite:///{self.SQLITE_DB_FILE}"
        raise ValueError("DB URL is undefined")

    @field_validator("SQLITE_DB_FILE", mode="after")
    @classmethod
    def check_sqlite_file(cls, file_name: str | None) -> str | None:
        if file_name is None or file_name == "" or Path(file_name).is_file():
            return file_name
        else:
            raise ValueError("Inconsistent SQLite DB file path")


class Settings(DBSetiings):
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
