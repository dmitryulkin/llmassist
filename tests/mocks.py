from typing import Tuple, Type

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

from src.utils import settings


class TestSettings(settings.Settings):
    # read only __init__ parameters
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
        return (init_settings,)
