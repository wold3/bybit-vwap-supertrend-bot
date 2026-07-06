import time
import logging
import requests
import subprocess

logger = logging.getLogger(__name__)


class Watchdog:

    def __init__(self, health_url="http://localhost:5000/health"):

        self.health_url = health_url
        self.fail_count = 0
        self.max_fail = 3

    # =====================================================
    # Health Check
    # =====================================================
    def check_health(self):

        try:
            res = requests.get(self.health_url, timeout=3)

            if res.status_code == 200:
                return True

        except Exception as e:
            logger.error("Health check failed: %s", e)

        return False

    # =====================================================
    # Restart Bot
    # =====================================================
    def restart_bot(self):

        logger.warning("Restarting trading bot...")

        try:
            subprocess.run(
                ["docker", "restart", "bybit_trading_bot"],
                check=True
            )

        except Exception as e:
            logger.error("Restart failed: %s", e)

    # =====================================================
    # Run Loop
    # =====================================================
    def run(self):

        logger.info("Watchdog started")

        while True:

            healthy = self.check_health()

            if not healthy:
                self.fail_count += 1
                logger.warning("Health fail count: %s", self.fail_count)

            else:
                self.fail_count = 0

            if self.fail_count >= self.max_fail:
                self.restart_bot()
                self.fail_count = 0

            time.sleep(10)


if __name__ == "__main__":

    watchdog = Watchdog()
    watchdog.run()
