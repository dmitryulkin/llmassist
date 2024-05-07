import asyncio
import sys
import traceback

from loguru import logger

from src.aiogram_bot.bot import AIOgramBot
from src.context import ctx

aiogram_bot = None


def init_context() -> None:
    try:
        ctx.init()
    except Exception:
        logger.error("Error during application init:")
        traceback.print_exc()
        exit(-1)


def init_ui() -> None:
    try:
        if ctx.settings.TGBOT_TOKEN:
            logger.info("Aiogram bot init...")
            global aiogram_bot
            aiogram_bot = AIOgramBot()
            logger.info("Aiogram bot init done")
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
    logger.info("App starting...")
    async with asyncio.TaskGroup() as tg:
        tg.create_task(console_mgmt())
        tg.create_task(aiogram_bot.start())
    logger.info("App stopped")


if __name__ == "__main__":
    asyncio.run(main())
