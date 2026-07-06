import logging
from datetime import datetime


def setup_logger():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("bot.log"),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger("BOT")


logger = setup_logger()
