import asyncio
import traceback
from logging import Logger

from src.utils.context import ctx
from src.utils.loggers import get_logger

logger: Logger | None = None


async def main() -> None:
    pass


if __name__ == "__main__":
    try:
        ctx.init()
        logger = get_logger(__name__)
    except Exception:
        print("Error during application initialization.")
        traceback.print_exc()
        exit(-1)

    logger.info("Start application")
    asyncio.run(main())
