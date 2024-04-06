import logging
from logging import getLogger

logger = getLogger(__name__)

logger.setLevel(logging.DEBUG)

logger.info("Logger initialized")

if __name__ == '__main__':
    logger.info("main function called")
