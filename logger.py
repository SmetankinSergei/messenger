from loguru import logger
import sys
import os

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
