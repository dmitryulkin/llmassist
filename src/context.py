from logging import Logger
from typing import Any

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

        # Logger uses ctx.settings and imported here to avoid circular import
        from src.utils.loggers import get_logger

        logger: Logger = get_logger(__name__)
        logger.info("Context init...")

        # ProxyManager uses ctx.settings and imported here
        # to avoid circular import
        from src.utils.proxies.manager import ProxyManager

        self.proxy_manager = ProxyManager()

        logger.info("Context init done")


ctx: Context = Context()
