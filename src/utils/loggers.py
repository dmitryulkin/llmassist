import logging
from pathlib import Path

from src.utils.context import ctx

_log_format: str = (
    "%(asctime)s - [%(levelname)s] - %(name)s - "
    + "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)


def _get_file_handler(level: int, log_path: Path):
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def _get_stream_handler(level: int):
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(name: str) -> logging.Logger:
    sets = ctx.settings
    logger = logging.getLogger(name)
    logger.setLevel(sets.LOG_LEVEL)
    logger.addHandler(_get_stream_handler(sets.LOG_LEVEL))
    if sets.LOG_TO_FILE:
        # the logger level should be as permissive
        # as the most permissive handler
        if sets.LOG_FILE_LEVEL < sets.LOG_LEVEL:
            logger.setLevel(sets.LOG_FILE_LEVEL)
        logger.addHandler(
            _get_file_handler(sets.LOG_FILE_LEVEL, sets.LOG_FILE)
        )
    return logger
