import logging
import os

def get_logger(name: str):
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s %(name)s - %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    return logger