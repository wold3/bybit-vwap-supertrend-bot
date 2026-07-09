import threading
import time

from utils.logger import (
    bot_logger,
    error_logger,
)


class Watchdog:

    def __init__(self):

        self.running = False
        self.thread = None

        self.interval = 30

        self.last_tick = time.time()

    # =====================================================
    # HEARTBEAT
    # =====================================================

    def heartbeat(self):

        self.last_tick = time.time()

    # =====================================================
    # START
    # =====================================================

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._loop,
            daemon=True,
        )

        self.thread.start()

        print("[WATCHDOG START]")

        bot_logger.info("WATCHDOG START")

    # =====================================================
    # LOOP
    # =====================================================

    def _loop(self):

        while self.running:

            try:

                elapsed = time.time() - self.last_tick

                if elapsed > self.interval * 2:

                    print(
                        "[WATCHDOG WARNING] No heartbeat "
                        f"for {elapsed:.1f}s"
                    )

                    bot_logger.warning(
                        f"No heartbeat for {elapsed:.1f}s"
                    )

                else:

                    print("[WATCHDOG OK]")

                time.sleep(self.interval)

            except Exception as e:

                print("[WATCHDOG ERROR]", e)

                error_logger.exception(str(e))

                time.sleep(5)

    # =====================================================
    # STOP
    # =====================================================

    def stop(self):

        self.running = False

        print("[WATCHDOG STOP]")

        bot_logger.info("WATCHDOG STOP")


watchdog = Watchdog()
