from pathlib import Path
from typing import Literal, Tuple, Type

from pydantic import PositiveInt
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

type LogLevelsAllowed = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class Settings(BaseSettings):
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
