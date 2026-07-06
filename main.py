import logging
import threading
import time

from api.websocket_client import ws_client
from services.event_bus import event_bus
from execution_worker import worker_loop

from services.watchdog_service import watchdog
from services.telegram_service import init_telegram


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


# =====================================================
# INIT
# =====================================================
def init_system():

    logger.info("SYSTEM INIT START")

    init_telegram("TOKEN", "CHAT_ID")

    watchdog.start()

    logger.info("SYSTEM READY")


# =====================================================
# ENTRY
# =====================================================
if __name__ == "__main__":

    init_system()

    # -------------------------
    # worker thread (event-driven engine)
    # -------------------------
    t = threading.Thread(target=worker_loop, daemon=True)
    t.start()

    # -------------------------
    # websocket start
    # -------------------------
    ws_client.start()

    logger.info("SYSTEM RUNNING (EVENT-DRIVEN)")

    # keep alive
    while True:
        time.sleep(10)
