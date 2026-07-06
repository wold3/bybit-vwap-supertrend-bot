import threading
import time
import logging
import atexit
import os
import sys

from worker import loop
from websocket_client import ws_client


# =========================================================
# LOGGER
# =========================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("BOT")


# =========================================================
# SINGLETON LOCK (중복 실행 방지)
# =========================================================
LOCK_FILE = "bot.lock"


def check_single_instance():

    if os.path.exists(LOCK_FILE):

        print("❌ BOT already running (lock file exists)")
        sys.exit(0)

    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))


def release_lock():

    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)


# =========================================================
# CLEAN EXIT REGISTER
# =========================================================
atexit.register(release_lock)


# =========================================================
# WORKER START
# =========================================================
def start_worker():

    t = threading.Thread(
        target=loop,
        daemon=True
    )

    t.start()

    logger.info("Worker started")


# =========================================================
# WEBSOCKET START
# =========================================================
def start_ws():

    ws_client.start()

    logger.info("WebSocket started")


# =========================================================
# SYSTEM INIT
# =========================================================
def init_system():

    logger.info("====================================")
    logger.info("     AUTO TRADING BOT START         ")
    logger.info("====================================")


# =========================================================
# MAIN ENTRY
# =========================================================
if __name__ == "__main__":

    try:

        # 🔥 핵심: 중복 실행 방지
        check_single_instance()

        init_system()

        start_worker()
        start_ws()

        logger.info("SYSTEM RUNNING (SINGLE INSTANCE MODE)")

        # KEEP ALIVE LOOP
        while True:
            time.sleep(10)

    except KeyboardInterrupt:

        logger.warning("SYSTEM STOPPED BY USER")

    except Exception as e:

        logger.error(f"FATAL ERROR: {e}")

    finally:

        release_lock()
