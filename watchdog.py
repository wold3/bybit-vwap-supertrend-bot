import time
import os
import subprocess
import psutil
from telegram import telegram


class Watchdog:

    def __init__(self):

        self.process_name = "main.py"
        self.restart_cmd = ["python", "main.py"]

        self.max_cpu = 90
        self.max_memory = 90

    # =================================================
    # PROCESS CHECK
    # =================================================
    def is_running(self):

        for proc in psutil.process_iter(['cmdline']):

            try:
                cmd = proc.info['cmdline']

                if cmd and "main.py" in " ".join(cmd):
                    return True

            except:
                continue

        return False

    # =================================================
    # RESOURCE CHECK
    # =================================================
    def system_ok(self):

        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent

        print(f"[WATCHDOG] CPU={cpu}% MEM={mem}%")

        if cpu > self.max_cpu or mem > self.max_memory:
            return False

        return True

    # =================================================
    # RESTART SYSTEM
    # =================================================
    def restart(self):

        telegram.send("⚠️ SYSTEM RESTARTING (WATCHDOG)")

        print("[WATCHDOG] RESTARTING SYSTEM...")

        subprocess.Popen(self.restart_cmd)


    # =================================================
    # MAIN LOOP
    # =================================================
    def run(self):

        while True:

            try:

                time.sleep(10)

                # 1. process check
                if not self.is_running():
                    print("[WATCHDOG] MAIN NOT RUNNING")
                    self.restart()
                    continue

                # 2. system health
                if not self.system_ok():
                    print("[WATCHDOG] HIGH LOAD DETECTED")
                    self.restart()
                    continue

            except Exception as e:

                print("[WATCHDOG ERROR]", e)
                telegram.send(f"❌ WATCHDOG ERROR: {e}")


# RUN
if __name__ == "__main__":

    w = Watchdog()
    w.run()
