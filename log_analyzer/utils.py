import logging
from logging import Logger
from typing import List, Optional


def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None) -> Logger:
    """Configure root logger with console and optional file handler."""
    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
    )

    handlers: List[logging.Handler] = []

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    handlers.append(stream_handler)

    if log_file is not None:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    for handler in handlers:
        logger.addHandler(handler)

    return logger
