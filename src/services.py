import sys

from loguru import logger
from pydantic import BaseModel

from src.aiogram_bot.bot import AIOgramBot
from src.db.db import DB
from src.utils.llms.llm import LLM
from src.utils.proxies.manager import ProxyManager
from src.utils.settings import Settings


class Services(BaseModel):
    """Application global resources environment.
    Main reason for this classis the opportunity to
    substitute global resources on testing.
    """

    _settings: Settings | None = None
    _db: DB | None = None
    _llm: LLM | None = None
    _proxy: ProxyManager | None = None
    _aiogram_bot: AIOgramBot | None = None

    @property
    def settings(self) -> Settings:
        assert self._settings is not None, "App Settings not init"
        return self._settings

    @settings.setter
    def settings(self, settings: Settings) -> None:
        self._settings = settings

    @property
    def db(self) -> DB:
        assert self._db is not None, "App DB not init"
        return self._db

    @property
    def llm(self) -> LLM:
        assert self._llm is not None, "LLM not init"
        return self._llm

    @property
    def proxy(self) -> ProxyManager:
        assert self._proxy is not None, "App Proxy Manager not init"
        return self._proxy

    @property
    def aiogram_bot(self) -> AIOgramBot:
        assert self._aiogram_bot is not None, "Aiogram Bot not init"
        return self._aiogram_bot

    async def init(self) -> None:
        """Explicit initialization"""

        if not self._settings:
            self._settings = Settings()

        self.init_loggers(self.settings)

        logger.info("Config init...")
        await self.init_db(self.settings)
        self.init_llm(self.settings)
        await self.init_proxies(self.settings)
        await self.init_aiogram_bot(self.settings)
        logger.info("Config init done")

    def init_loggers(self, settings: Settings):
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
        logger.add(sys.stdout, level=settings.LOG_LEVEL, format=format)

        if settings.LOG_TO_FILE:
            file_format = (
                "{time} - [{level: <8}] - {message} - {name}:{function}:{line}"
            )
            logger.add(
                settings.LOG_FILE,
                level=settings.LOG_FILE_LEVEL,
                format=file_format,
                rotation="100 KB",
                compression="zip",
            )

    async def init_db(self, settings: Settings) -> None:
        self._db = DB(settings=settings)
        await self.db.init()
        await self.db.check()

    def init_llm(self, settings: Settings) -> None:
        self._llm = LLM(settings=settings)
        self.llm.init()

    async def init_proxies(self, settings: Settings) -> None:
        self._proxy = ProxyManager(settings=settings)
        await self.proxy.init()

    async def init_aiogram_bot(self, settings: Settings) -> None:
        if self.settings.TGBOT_TOKEN:
            self._aiogram_bot = AIOgramBot(settings=settings)
            await self.aiogram_bot.init()


srv: Services = Services()
