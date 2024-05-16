from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger
from pydantic import BaseModel

from src.utils.settings import Settings


class AIOgramBot(BaseModel):
    settings: Settings
    _bot: Bot | None = None
    _dp: Dispatcher | None = None

    @property
    def bot(self) -> Bot:
        assert self._bot is not None, "Aiogram Bot not init"
        return self._bot

    @property
    def dp(self) -> Dispatcher:
        assert self._dp is not None, "Aiogram Dispatcher not init"
        return self._dp

    async def init(self) -> None:
        logger.info("Aiogram bot init...")
        if self.settings.TGBOT_TOKEN is None:
            raise ValueError("TGBOT_TOKEN not specified")
        self._bot = Bot(
            token=self.settings.TGBOT_TOKEN, parse_mode=ParseMode.HTML
        )
        self._dp = Dispatcher(storage=MemoryStorage())
        logger.info("Aiogram bot init done")

    async def start(self) -> None:
        self.dp.startup.register(self._on_startup)
        self.dp.shutdown.register(self._on_shutdown)
        await self.dp.start_polling(
            self.bot, allowed_updates=self.dp.resolve_used_update_types()
        )

    async def _on_startup(self) -> None:
        logger.info("Aiogram bot starting...")

        # TODO
        # register_middlewares(dp)
        # dp.include_router(get_handlers_router())
        # await set_default_commands(bot)

        bot_info = await self.bot.get_me()

        logger.info(f"Name     - {bot_info.full_name}")
        logger.info(f"Username - @{bot_info.username}")
        logger.info(f"ID       - {bot_info.id}")

        states: dict[bool | None, str] = {
            True: "Enabled",
            False: "Disabled",
            None: "Unknown (This's not a bot)",
        }

        logger.info(f"Groups Mode  - {states[bot_info.can_join_groups]}")
        logger.info(
            f"Privacy Mode - "
            f"{states[not bot_info.can_read_all_group_messages]}"
        )
        logger.info(
            f"Inline Mode  - {states[bot_info.supports_inline_queries]}"
        )

        logger.info("Aiogram bot started")

    async def _on_shutdown(self) -> None:
        logger.info("Aiogram bot stopping...")

        # TODO
        # await remove_default_commands(bot)

        await self.dp.storage.close()
        await self.dp.fsm.storage.close()

        await self.bot.delete_webhook()
        await self.bot.session.close()

        logger.info("Aiogram bot stopped")
