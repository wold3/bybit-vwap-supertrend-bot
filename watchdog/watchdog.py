import threading
import time


class Watchdog:
    """
    Bot system watchdog

    기능:
    - heartbeat 기록
    - 서비스 상태 확인
    - 생존 여부 확인
    """

    def __init__(self):

        self.running = False

        self.last_heartbeat = 0

        # RLock 사용 (status -> is_alive 데드락 방지)
        self.lock = threading.RLock()



    def start(self):

        with self.lock:

            self.running = True
            self.last_heartbeat = time.time()

        print("[Watchdog] started")

        return True



    def stop(self):

        with self.lock:

            self.running = False

        print("[Watchdog] stopped")

        return True



    def heartbeat(self):

        with self.lock:

            self.last_heartbeat = time.time()

        return True



    def is_alive(self, timeout=60):

        with self.lock:

            if not self.running:
                return False

            return (
                time.time() - self.last_heartbeat
            ) <= timeout



    def status(self):

        with self.lock:

            elapsed = None

            if self.last_heartbeat:

                elapsed = (
                    time.time()
                    - self.last_heartbeat
                )

            return {

                "running": self.running,

                "alive": self.is_alive(),

                "last_heartbeat": self.last_heartbeat,

                "elapsed": elapsed

            }



    def reset(self):

        with self.lock:

            self.running = False
            self.last_heartbeat = 0

        return True



# ===========================================
# Singleton
# ===========================================

watchdog = Watchdog()
