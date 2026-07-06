import threading
import time

from worker import loop
from websocket_client import ws_client


if __name__ == "__main__":

    threading.Thread(target=loop, daemon=True).start()

    ws_client.start()

    print("🔥 FINAL AUTO TRADING SYSTEM RUNNING")

    while True:
        time.sleep(10)
