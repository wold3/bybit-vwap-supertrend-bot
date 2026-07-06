import time
import threading
import logging
import requests
import os
import subprocess

logger = logging.getLogger(__name__)


class WatchdogService:

    def __init__(self):

        self.health_url = "http://127.0.0.1:8000/health"
        self.check_interval = 30
        self.restart_command = ["python", "app.py"]

        self.last_ok = time.time()

    # =====================================================
    # Health Check
    # =====================================================
    def check_health(self):

        try:

            res = requests.get(
                self.health_url,
                timeout=5,
            )

            if res.status_code == 200:

                self.last_ok = time.time()
                return True

        except Exception:

            return False

        return False

    # =====================================================
    # Restart System
    # =====================================================
    def restart(self):

        logger.warning("System restart triggered")

        try:

            os.system("pkill -f app.py")

            time.sleep(2)

            subprocess.Popen(
                self.restart_command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        except Exception as e:

            logger.exception(e)

    # =====================================================
    # Monitor Loop
    # =====================================================
    def run(self):

        logger.info("Watchdog started")

        while True:

            try:

                healthy = self.check_health()

                if not healthy:

                    # 60초 이상 죽어있으면 재시작
                    if time.time() - self.last_ok > 60:

                        self.restart()

                        self.last_ok = time.time()

                time.sleep(self.check_interval)

            except Exception as e:

                logger.exception(e)
                time.sleep(10)


# =====================================================
# Singleton
# =====================================================
watchdog = WatchdogService()


# =====================================================
# Background Thread Starter
# =====================================================
def start_watchdog():

    t = threading.Thread(
        target=watchdog.run,
        daemon=True,
    )

    t.start()

    logger.info("Watchdog thread started")
