import sys

from loguru import logger

# logger
logger.remove(0)
logger.add(sys.stdout, backtrace=True, diagnose=True)


def log_step(step: str):
    logger.info("-" * 10)
    logger.info(step)
    logger.info("-" * 10)
