import threading
import time
import logging

from worker import loop
from websocket_client import ws_client

# ================================
# LOGGER
# ================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("BOT")


# ================================
# BOT START
# ================================
def start_bot():

    logger.info("STARTING AUTO TRADING BOT")

    # worker thread
    threading.Thread(target=loop, daemon=True).start()

    # websocket thread
    ws_client.start()

    logger.info("BOT ENGINE RUNNING")


# ================================
# MAIN
# ================================
if __name__ == "__main__":

    start_bot()

    logger.info("SYSTEM FULLY RUNNING")

    while True:
        time.sleep(10)
