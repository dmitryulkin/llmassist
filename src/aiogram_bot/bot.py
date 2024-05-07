from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.context import ctx
from src.exceptions import CustomError
from src.utils.loggers import get_logger

logger = get_logger(__name__)


class AIOgramBot:
    def __init__(self) -> None:
        if not ctx.settings.TGBOT_TOKEN:
            raise CustomError("TGBOT_TOKEN not specified")

        self.bot = Bot(
            token=ctx.settings.TGBOT_TOKEN, parse_mode=ParseMode.HTML
        )
        self.dp = Dispatcher(storage=MemoryStorage())

    async def start(self) -> None:
        logger.info("Start aiogram bot")
        await self.dp.start_polling(
            self.bot, allowed_updates=self.dp.resolve_used_update_types()
        )
