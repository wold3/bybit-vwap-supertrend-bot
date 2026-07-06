import threading
import time
import logging

from api.websocket_client import ws_client
from execution_worker import worker_loop

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
    logger.info("   v6 AUTO TRADING SYSTEM START   ")
    logger.info("===================================")


# =====================================================
# WORKER START
# =====================================================
def start_worker():

    t = threading.Thread(
        target=worker_loop,
        daemon=True
    )

    t.start()

    logger.info("Worker started")


# =====================================================
# WEBSOCKET START
# =====================================================
def start_websocket():

    ws_client.start()

    logger.info("WebSocket started")


# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":

    try:

        init_system()

        start_worker()

        start_websocket()

        logger.info("SYSTEM RUNNING...")

        # keep alive
        while True:
            time.sleep(10)

    except KeyboardInterrupt:

        logger.warning("SYSTEM STOPPED BY USER")

    except Exception as e:

        logger.error(f"FATAL ERROR: {e}")
