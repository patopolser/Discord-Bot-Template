import datetime

import logging
from logging import handlers

FMT = "%(asctime)s | [%(levelname)s] - %(message)s"

FORMATS = {
    logging.DEBUG: f"{FMT}",
    logging.INFO: f"\33[36m{FMT}\33[0m",
    logging.WARNING: f"\33[33m{FMT}\33[0m",
    logging.ERROR: f"\33[31m{FMT}\33[0m",
    logging.CRITICAL: f"\33[1m\33[31m{FMT}\33[0m"
}

class ConsoleFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_format = FORMATS[record.levelno]
        formatter = logging.Formatter(log_format, style="%")
        return formatter.format(record)

class FileFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_format = FMT
        formatter = logging.Formatter(log_format)
        return formatter.format(record)

now = datetime.datetime.now().strftime("%d-%m-%Y")

file_handler = handlers.RotatingFileHandler(filename= f"./logs/{now}.log")
file_handler.setFormatter(FileFormatter())

console_handler = logging.StreamHandler()
console_handler.setFormatter(ConsoleFormatter())

logging.basicConfig(
    level= logging.INFO,
    datefmt= "%d/%m/%Y %H:%M:%S",
    handlers=[file_handler, console_handler]
)
