import logging
import time
import threading

from execution.execution_engine import engine
from risk.risk_engine import get_risk_status
from telegram import send_error

logger = logging.getLogger(__name__)


class Watchdog:

    def __init__(self):

        self.last_check = time.time()
        self.interval = 10  # 10초마다 체크
        self.running = False

    # =====================================================
    # Health Check
    # =====================================================
    def check_system(self):

        try:

            # 1. Execution Engine 상태
            engine_status = engine.status()

            if not engine_status.get("running", True):
                raise Exception("Execution engine stopped")

            # 2. Risk Engine 상태
            risk = get_risk_status()

            if risk.get("daily_limit", False):
                logger.warning("Daily loss limit reached")

            # 3. 거래 멈춤 감지
            last_exec = engine_status.get("last_execution")

            if last_exec is None:
                raise Exception("No execution detected")

            logger.info("System OK")

            return True

        except Exception as e:

            logger.error("WATCHDOG ERROR: %s", str(e))

            send_error(f"Watchdog alert: {str(e)}")

            return False

    # =====================================================
    # Loop
    # =====================================================
    def run(self):

        self.running = True

        logger.info("Watchdog started")

        while self.running:

            self.check_system()

            time.sleep(self.interval)

    # =====================================================
    # Stop
    # =====================================================
    def stop(self):

        self.running = False

        logger.info("Watchdog stopped")


# =====================================================
# Singleton
# =====================================================
watchdog = Watchdog()


def start_watchdog():

    thread = threading.Thread(
        target=watchdog.run,
        daemon=True
    )

    thread.start()

    return thread
