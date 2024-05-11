import asyncio
import sys

from loguru import logger

from src.services import srv


async def console_mgmt() -> None:
    def print_red(msg: str) -> None:
        print(f"\033[91m {msg}\033[00m")

    print_red("Console is waiting for command:")
    while True:
        inp = (await asyncio.to_thread(sys.stdin.readline)).rstrip("\n")
        match inp:
            case "stop" | "close" | "0":
                if srv.aiogram_bot:
                    await srv.aiogram_bot.dp.stop_polling()
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
        srv.init()

    logger.info("App starting...")
    async with asyncio.TaskGroup() as tg:
        tg.create_task(console_mgmt())
        if srv.aiogram_bot:
            tg.create_task(srv.aiogram_bot.start())
    logger.info("App stopped")


if __name__ == "__main__":
    asyncio.run(main())
