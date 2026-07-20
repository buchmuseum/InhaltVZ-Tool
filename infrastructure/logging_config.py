"""
Zentrale Logging-Konfiguration.

Alle Module verwenden denselben Logger.
"""

import logging
from logging.handlers import RotatingFileHandler

from config.settings import (
    LOG_DIR,
    LOG_FILE
)


def setup_logging() -> None:

    LOG_DIR.mkdir(
        exist_ok=True
    )

    logger = logging.getLogger()

    logger.setLevel(
        logging.INFO
    )


    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8"
    )


    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )


    handler.setFormatter(
        formatter
    )


    logger.addHandler(
        handler
    )


    logging.info(
        "Logging gestartet"
    )