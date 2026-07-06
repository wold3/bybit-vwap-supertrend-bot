import threading
import time
import logging
import os
import webbrowser

from worker import loop
from websocket_client import ws_client
from utils.singleton import singleton


# =========================================================
# LOGGER
# =========================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("BOT")


# =========================================================
# DASHBOARD URL
# =========================================================
DASHBOARD_URL = "http://localhost:5000"


# =========================================================
# CHROME AUTO OPEN
# =========================================================
def open_chrome():

    time.sleep(3)

    try:
        os.system(f'start chrome "{DASHBOARD_URL}"')
        logger.info("Chrome opened")
    except Exception as e:
        logger.error(f"Chrome open failed: {e}")


# =========================================================
# WORKER START
# =========================================================
def start_worker():

    threading.Thread(
        target=loop,
        daemon=True
    ).start()

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
    logger.info("     AUTO TRADING START SYSTEM      ")
    logger.info("====================================")


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":

    try:

        # 🔥 싱글 인스턴스 보호
        singleton.acquire()

        init_system()

        # CORE ENGINE
        start_worker()
        start_ws()

        logger.info("SYSTEM RUNNING")

        # 🔥 크롬 자동 실행
        threading.Thread(target=open_chrome, daemon=True).start()

        # KEEP ALIVE
        while True:
            time.sleep(10)

    except KeyboardInterrupt:
        logger.warning("STOPPED BY USER")

    except Exception as e:
        logger.error(f"FATAL ERROR: {e}")
