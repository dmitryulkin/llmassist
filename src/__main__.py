import asyncio
import sys
import traceback

from src.context import ctx
from src.utils.loggers import get_logger

logger = None
aiogram_bot = None


def init_context() -> None:
    try:
        ctx.init()
        global logger
        logger = get_logger(__name__)
    except Exception:
        print("Error during application init:")
        traceback.print_exc()
        exit(-1)


def init_ui() -> None:
    try:
        if ctx.settings.TGBOT_TOKEN:
            logger.info("Init aiogram bot")
            from src.aiogram_bot.bot import AIOgramBot

            global aiogram_bot
            aiogram_bot = AIOgramBot()
            logger.info("Init aiogram bot done")
        else:
            logger.error("There are no active interfaces for usage")
    except Exception:
        print("Error during user interfaces init:")
        traceback.print_exc()
        exit(-1)


async def console_mgmt() -> None:
    def print_red(msg: str) -> None:
        print(f"\033[91m {msg}\033[00m")

    print_red("Console is waiting for command:")
    while True:
        inp = (await asyncio.to_thread(sys.stdin.readline)).rstrip("\n")
        match inp:
            case "stop" | "close" | "0":
                await aiogram_bot.dp.stop_polling()
                break
            case "help" | "?":
                print_red("stop | close | 0 - stop app")
            case _:
                print_red("Unrecognized command, try help | ?")


async def main() -> None:
    init_context()
    init_ui()
    logger.info("Start app")
    async with asyncio.TaskGroup() as tg:
        tg.create_task(console_mgmt())
        tg.create_task(aiogram_bot.start())
    logger.info("Stop app")


if __name__ == "__main__":
    asyncio.run(main())
