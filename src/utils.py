import time
import sys
import logging


def get_logger(filename):
    """Return a logger instance that writes in filename
    Args:
        filename: (string) path to log.txt
    Returns:
        logger: (instance of logger)
    """
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(
            '%(asctime)s:%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(handler)

    return logger
