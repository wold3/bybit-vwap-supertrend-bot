import os
import logging
from logging.handlers import RotatingFileHandler

# =====================================================
# LOG DIRECTORY
# =====================================================

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

# =====================================================
# FORMAT
# =====================================================

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

# =====================================================
# BOT LOGGER
# =====================================================

bot_logger = logging.getLogger("BOT")

bot_logger.setLevel(logging.INFO)

if not bot_logger.handlers:

    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "bot.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    bot_logger.addHandler(file_handler)
    bot_logger.addHandler(console_handler)

# =====================================================
# ERROR LOGGER
# =====================================================

error_logger = logging.getLogger("ERROR")

error_logger.setLevel(logging.ERROR)

if not error_logger.handlers:

    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "error.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    error_logger.addHandler(file_handler)
    error_logger.addHandler(console_handler)

# =====================================================
# START LOG
# =====================================================

bot_logger.info("Logger initialized")
