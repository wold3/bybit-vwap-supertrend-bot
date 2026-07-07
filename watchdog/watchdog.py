import time
import threading


class Watchdog:
    """
    Bot system watchdog

    기능:
    - heartbeat 기록
    - 프로세스 상태 확인
    - 서비스 생존 체크
    - 외부 모듈 import 호환
    """


    def __init__(self):

        self.running = False
        self.last_heartbeat = 0
        self.lock = threading.Lock()



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

            elapsed = time.time() - self.last_heartbeat

        return elapsed <= timeout



    def status(self):

        with self.lock:

            elapsed = (
                time.time() - self.last_heartbeat
                if self.last_heartbeat
                else None
            )

            return {
                "running": self.running,
                "alive": self.is_alive(),
                "last_heartbeat": self.last_heartbeat,
                "elapsed": elapsed
            }



# =================================================
# GitHub style singleton object
#
# 사용:
# from watchdog.watchdog import watchdog
# =================================================

watchdog = Watchdog()
