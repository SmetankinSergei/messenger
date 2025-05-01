import sys
import os
import logging
from loguru import logger

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger.remove()

logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG"
)

logger.add(
    f"{LOG_DIR}/app.log",
    rotation="1 week",
    retention="4 weeks",
    compression="zip",
    encoding="utf-8",
    level="INFO"
)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = record.levelname
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=logging.DEBUG)
