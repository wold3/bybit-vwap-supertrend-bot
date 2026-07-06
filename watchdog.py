import threading
import time
import os


# ================================
# SIMPLE WATCHDOG
# ================================
def monitor():

    while True:

        # 여기에 상태 체크 로직 추가 가능
        print("[WATCHDOG] SYSTEM ALIVE")

        time.sleep(10)


def start_watchdog():

    t = threading.Thread(target=monitor, daemon=True)
    t.start()
