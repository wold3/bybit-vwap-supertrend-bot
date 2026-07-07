import time
import threading

try:
    import psutil
except ImportError:
    psutil = None


try:
    from telegram import telegram
except ImportError:
    telegram = None



class Watchdog:
    """
    Bot Watchdog Service

    기능:
    - 실행 상태 관리
    - heartbeat 감시
    - 시스템 상태 확인
    - Telegram 알림 연동
    """


    def __init__(self):

        self.running = True
        self.start_time = time.time()
        self.last_heartbeat = time.time()
        self.lock = threading.Lock()



    def heartbeat(self):

        with self.lock:
            self.last_heartbeat = time.time()

        return True



    def is_alive(self, timeout=60):

        with self.lock:
            diff = time.time() - self.last_heartbeat

        return diff <= timeout



    def status(self):

        with self.lock:

            uptime = int(
                time.time() - self.start_time
            )

            heartbeat_age = (
                time.time()
                -
                self.last_heartbeat
            )


        data = {
            "running": self.running,
            "uptime": uptime,
            "alive": heartbeat_age < 60,
            "heartbeat_age": heartbeat_age
        }


        if psutil:

            data.update({
                "cpu": psutil.cpu_percent(),
                "memory": psutil.virtual_memory().percent
            })


        return data



    def start(self):

        self.running = True
        self.heartbeat()

        print("[Watchdog] started")

        return True



    def stop(self):

        self.running = False

        print("[Watchdog] stopped")

        return True



    def notify(self, message):

        if telegram:

            try:
                telegram.send(message)

            except Exception:
                pass



# 외부 import용 객체
watchdog = Watchdog()
