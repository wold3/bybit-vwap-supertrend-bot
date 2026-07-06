import logging
import threading
import time

from api.websocket_client import ws_client
from execution_worker import worker_loop

from services.watchdog_service import watchdog
from services.telegram_service import init_telegram

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_system():

    logger.info("SYSTEM INIT START")

    init_telegram("TOKEN", "CHAT_ID")

    watchdog.start()

    logger.info("SYSTEM READY")


if __name__ == "__main__":

    init_system()

    threading.Thread(target=worker_loop, daemon=True).start()

    ws_client.start()

    logger.info("TRADING ENGINE RUNNING")

    while True:
        time.sleep(10)
