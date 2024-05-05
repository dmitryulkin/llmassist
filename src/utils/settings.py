import logging
from pathlib import Path
from typing import Tuple, Type

from pydantic import PositiveInt, ValidationInfo, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    # secrets

    # .env
    # general settings
    LOG_LEVEL: int = logging.DEBUG
    LOG_TO_FILE: bool = False
    LOG_FILE: Path = Path("llmassist.log")
    LOG_FILE_LEVEL: int = logging.DEBUG

    # proxy settings
    # tor
    USE_TOR: bool = False
    TOR_SOCKS5_PORT: PositiveInt | None = None

    @field_validator("LOG_LEVEL", "LOG_FILE_LEVEL", mode="before")
    @classmethod
    def transform_log_level_str_to_int(
        cls, value: int | str, info: ValidationInfo
    ) -> int:
        value = value.casefold() if type(value) is str else value
        match value:
            case "debug" | logging.DEBUG:
                return logging.DEBUG
            case "info":
                return logging.INFO
            case "warn" | "warning":
                return logging.WARNING
            case "error":
                return logging.ERROR
            case _:
                raise ValueError(f".env {info.field_name} is incorrect")

    @field_validator("TOR_SOCKS5_PORT", mode="after")
    @classmethod
    def check_tor_port(
        cls, value: PositiveInt | None, info: ValidationInfo
    ) -> PositiveInt | None:
        if info.data["USE_TOR"]:
            assert (
                value
            ), "TOR_SOCKS5_PORT is required because of .env USE_TOR=True"
        return value

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
