import threading
import time
import logging

from worker import loop
from websocket_client import ws_client

logging.basicConfig(level=logging.INFO)


def start():

    threading.Thread(target=loop, daemon=True).start()
    ws_client.start()

    print("SYSTEM STARTED")


if __name__ == "__main__":

    start()

    while True:
        time.sleep(10)
