import os
import logging


def setupLogger():
    logging.basicConfig(
        format='%(asctime)s %(name)-35s %(levelname)-8s %(message)s',
        level=logging.ERROR
    )


def getLogger(logger_name):
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.getLevelName(LOG_LEVEL))

    return logger
