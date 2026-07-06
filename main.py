import threading
import time
import logging

from worker import loop
from websocket_client import ws_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


# =====================================================
# SYSTEM INIT
# =====================================================
def init_system():

    logger.info("===================================")
    logger.info("   AUTO TRADING SYSTEM STARTING   ")
    logger.info("===================================")


# =====================================================
# START WORKER
# =====================================================
def start_worker():

    t = threading.Thread(
        target=loop,
        daemon=True
    )

    t.start()

    logger.info("Worker started")


# =====================================================
# START WEBSOCKET
# =====================================================
def start_ws():

    ws_client.start()

    logger.info("WebSocket started")


# =====================================================
# MAIN ENTRY
# =====================================================
if __name__ == "__main__":

    try:

        init_system()

        start_worker()

        start_ws()

        logger.info("SYSTEM RUNNING...")

        # keep alive loop
        while True:
            time.sleep(10)

    except KeyboardInterrupt:

        logger.warning("SYSTEM STOPPED (KeyboardInterrupt)")

    except Exception as e:

        logger.error(f"FATAL ERROR: {e}")
