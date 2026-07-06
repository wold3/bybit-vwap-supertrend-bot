import threading
import time
import logging

from api.websocket_client import ws_client
from execution_worker import worker_loop
from services.watchdog_service import watchdog

logging.basicConfig(level=logging.INFO)


def init():
    watchdog.start()


if __name__ == "__main__":

    init()

    threading.Thread(target=worker_loop, daemon=True).start()

    ws_client.start()

    print("🔥 v5 HFT-LITE RUNNING")

    while True:
        time.sleep(10)
