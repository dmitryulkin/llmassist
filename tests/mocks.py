from typing import Tuple, Type

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

from src.utils.settings import Settings


class SettingsMock(Settings, validate_assignment=True):
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
        # here we choose to ignore arguments other then from init_settings
        return (init_settings,)
