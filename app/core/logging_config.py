import logging
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler(
    filename="app_log.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=2,
    mode="w",
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[file_handler],
)

logger = logging.getLogger("invoice_app")