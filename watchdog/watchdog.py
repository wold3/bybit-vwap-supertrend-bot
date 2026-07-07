import time
import threading


class Watchdog:
    """
    시스템 상태 감시 모듈

    - heartbeat 기록
    - 실행 상태 확인
    - 서비스 생존 확인
    """

    def __init__(self):
        self.running = True
        self.last_heartbeat = time.time()
        self.lock = threading.Lock()


    def heartbeat(self):
        """
        heartbeat 갱신
        """

        with self.lock:
            self.last_heartbeat = time.time()

        return True


    def is_alive(self, timeout=60):
        """
        마지막 heartbeat 이후
        timeout 초 이내인지 확인
        """

        with self.lock:
            elapsed = time.time() - self.last_heartbeat

        return elapsed < timeout


    def status(self):
        """
        현재 상태 반환
        """

        with self.lock:
            elapsed = time.time() - self.last_heartbeat

        return {
            "running": self.running,
            "alive": self.is_alive(),
            "last_heartbeat": self.last_heartbeat,
            "elapsed": elapsed
        }


    def stop(self):
        """
        watchdog 종료
        """

        self.running = False


    def start(self):
        """
        watchdog 시작
        """

        self.running = True
        self.heartbeat()

        print("[Watchdog] started")

        return True



# =================================================
# 외부 모듈 import용 객체
#
# 사용:
# from watchdog.watchdog import watchdog
# =================================================

watchdog = Watchdog()
