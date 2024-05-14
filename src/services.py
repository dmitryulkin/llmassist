import sys
from dataclasses import dataclass

from loguru import logger

from src.utils.settings import Settings


@dataclass
class Services:
    """Application global resources environment.
    Main reason for this classis the opportunity to
    substitute global resources on testing.
    """

    settings = None
    db = None
    proxy_manager = None
    aiogram_bot = None

    async def init(self) -> None:
        """Explicit initialization"""

        if not self.settings:
            self.settings = Settings()

        self.init_loggers()

        logger.info("Config init...")
        await self.init_db()
        self.init_proxies()
        self.init_aiogram_bot()
        logger.info("Config init done")

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

    async def init_db(self) -> None:
        from src.db.db import DB

        self.db = DB()
        await self.db.check()

    def init_proxies(self) -> None:
        from src.utils.proxies.manager import ProxyManager

        self.proxy_manager = ProxyManager()

    def init_aiogram_bot(self) -> None:
        if srv.settings.TGBOT_TOKEN:
            from src.aiogram_bot.bot import AIOgramBot

            logger.info("Aiogram bot init...")
            self.aiogram_bot = AIOgramBot()
            logger.info("Aiogram bot init done")


srv: Services = Services()
