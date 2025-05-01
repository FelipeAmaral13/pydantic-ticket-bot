import logging
from logging.handlers import RotatingFileHandler
import sys

# Logger base
logger = logging.getLogger("ticket_system_logger")
logger.setLevel(logging.DEBUG)

# File handler (log em arquivo, já estava OK)
file_handler = RotatingFileHandler(
    "ticket_system.log",
    maxBytes=1024 * 1024 * 5,
    backupCount=3,
    encoding='utf-8'  # <== importante!
)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Stream handler para console com UTF-8
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
console_handler.stream.reconfigure(encoding='utf-8')  # <== crucial para Windows
logger.addHandler(console_handler)

# Funções de log
def log_info(message): logger.info(message)
def log_warning(message): logger.warning(message)
def log_error(message): logger.error(message)
def log_debug(message): logger.debug(message)
