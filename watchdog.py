import subprocess
import time
import signal
import sys
import requests


HEALTH_URL = "http://127.0.0.1:5000/health"

CHECK_INTERVAL = 10

MAX_RESTART = 20


class WatchDog:

    def __init__(self):

        self.process = None

        self.restart_count = 0

        self.running = True

    # ----------------------------------------

    def start_bot(self):

        print("[WatchDog] Starting bot...")

        self.process = subprocess.Popen(
            [sys.executable, "app.py"]
        )

    # ----------------------------------------

    def stop_bot(self):

        if self.process is None:
            return

        if self.process.poll() is None:

            print("[WatchDog] Stopping bot...")

            self.process.terminate()

            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()

    # ----------------------------------------

    def restart_bot(self):

        self.stop_bot()

        time.sleep(2)

        self.start_bot()

        self.restart_count += 1

    # ----------------------------------------

    def health_check(self):

        try:

            r = requests.get(
                HEALTH_URL,
                timeout=3,
            )

            return r.status_code == 200

        except Exception:

            return False

    # ----------------------------------------

    def run(self):

        self.start_bot()

        while self.running:

            if self.restart_count >= MAX_RESTART:

                print(
                    "[WatchDog] Restart limit exceeded."
                )

                break

            if not self.health_check():

                print(
                    "[WatchDog] Health check failed."
                )

                self.restart_bot()

            time.sleep(CHECK_INTERVAL)

        self.stop_bot()


watchdog = WatchDog()


def shutdown(sig, frame):

    print("\n[WatchDog] Shutdown")

    watchdog.running = False


signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)


if __name__ == "__main__":

    watchdog.run()
