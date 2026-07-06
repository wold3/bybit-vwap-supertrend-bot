import logging
import os
from datetime import datetime


class LoggerService:

    def __init__(self):

        self.logger = logging.getLogger("trading_bot")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:

            os.makedirs("logs", exist_ok=True)

            file_handler = logging.FileHandler(
                f"logs/bot_{datetime.utcnow().date()}.log"
            )

            console_handler = logging.StreamHandler()

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )

            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    # =====================================================
    # Info Log
    # =====================================================
    def info(self, message, *args):

        self.logger.info(message, *args)

    # =====================================================
    # Warning Log
    # =====================================================
    def warning(self, message, *args):

        self.logger.warning(message, *args)

    # =====================================================
    # Error Log
    # =====================================================
    def error(self, message, *args):

        self.logger.error(message, *args)

    # =====================================================
    # Exception Log
    # =====================================================
    def exception(self, message, *args):

        self.logger.exception(message, *args)


# =====================================================
# Singleton
# =====================================================
logger_service = LoggerService()
