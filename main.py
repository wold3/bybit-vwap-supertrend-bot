import time
import threading
import logging

from api.websocket_client import ws_client
from execution_worker import worker_loop
from services.watchdog_service import watchdog
from services.telegram_service import init_telegram

logging.basicConfig(level=logging.INFO)


def init_system():
    init_telegram("TOKEN", "CHAT_ID")
    watchdog.start()


if __name__ == "__main__":

    init_system()

    threading.Thread(target=worker_loop, daemon=True).start()

    ws_client.start()

    print("TRADING ENGINE STARTED")

    while True:
        time.sleep(10)
