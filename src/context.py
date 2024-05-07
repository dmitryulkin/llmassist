import sys
from typing import Any

from loguru import logger
from pydantic import BaseModel

from src.utils.settings import Settings


class Context(BaseModel):
    """Application global resources environment"""

    settings: Settings | None = None
    proxy_manager: Any = None

    def init(self) -> None:
        """Explicit initialization"""

        if not self.settings:
            self.settings = Settings()

        self.init_loggers()

        logger.info("Context init...")

        # ProxyManager uses ctx.settings and imported here
        # to avoid circular import
        from src.utils.proxies.manager import ProxyManager

        self.proxy_manager = ProxyManager()

        logger.info("Context init done")

    def init_loggers(self):
        """
        Initialize loggers:
        - sys.stdout
        - LOG_FILE
        """
        format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
            "- [<level>{level: <8}</level>] - <level>{message}</level> "
            "- <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
        )
        logger.remove(0)
        logger.add(sys.stdout, level=self.settings.LOG_LEVEL, format=format)

        if self.settings.LOG_TO_FILE:
            file_format = (
                "{time} - [{level: <8}] - {message} - {name}:{function}:{line}"
            )
            logger.add(
                self.settings.LOG_FILE,
                level=self.settings.LOG_FILE_LEVEL,
                format=file_format,
                rotation="100 KB",
                compression="zip",
            )


ctx: Context = Context()
