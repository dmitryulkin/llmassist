import asyncio
import sys

from loguru import logger

from src.aiogram_bot.bot import AIOgramBot
from src.context import ctx

aiogram_bot = None


def init_ui() -> None:
    if ctx.settings.TGBOT_TOKEN:
        logger.info("Aiogram bot init...")
        global aiogram_bot
        aiogram_bot = AIOgramBot()
        logger.info("Aiogram bot init done")
    else:
        logger.error("There are no active interfaces for usage")


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
    with logger.catch(
        level="CRITICAL",
        message="Error during app context init",
        onerror=lambda _: sys.exit(-1),
    ):
        ctx.init()
        init_ui()

    logger.info("App starting...")
    async with asyncio.TaskGroup() as tg:
        tg.create_task(console_mgmt())
        tg.create_task(aiogram_bot.start())
    logger.info("App stopped")


if __name__ == "__main__":
    asyncio.run(main())
