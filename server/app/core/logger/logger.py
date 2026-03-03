import logging
from app.core.logger.json_formatter import JSONFormatter
import sys
import queue
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
import os
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent

def init_logging():
    """
    Initalizes and configures the logging service: formatters, handlers and loggers.
    """
    print(BASE_DIR)
    config_file = Path(BASE_DIR / "logger_config.json")
    with open(config_file) as f:
        config = json.load(f)
    logging.config.dictConfig(config)



        