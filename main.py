
import threading
import time
from dotenv import load_dotenv

from execution.execution_engine import BybitExecutionEngine
from strategy.strategy_engine import StrategyEngine

from services.ws_client import start_ws
from services.fill_ws import start_fill_ws

from watchdog import Watchdog
from telegram import telegram

from portfolio.position_sync import position_sync


# =================================================
# ENV LOAD
# =================================================
load_dotenv()


# =================================================
# CORE ENGINE INIT
# =================================================
execution_engine = BybitExecutionEngine()
strategy_engine = StrategyEngine(execution_engine)


# =================================================
# MARKET WS
# =================================================
def run_market_ws():

    try:
        start_ws(strategy_engine)

    except Exception as e:
        print("[MARKET WS ERROR]", e)
        telegram.send(f"❌ MARKET WS ERROR: {e}")


# =================================================
# FILL WS
# =================================================
def run_fill_ws():

    try:
        start_fill_ws()

    except Exception as e:
        print("[FILL WS ERROR]", e)
        telegram.send(f"❌ FILL WS ERROR: {e}")


# =================================================
# HEARTBEAT
# =================================================
def heartbeat():

    while True:

        try:
            time.sleep(30)
            print("[HEARTBEAT] SYSTEM OK")

        except Exception as e:
            print("[HEARTBEAT ERROR]", e)
            telegram.send(f"❌ HEARTBEAT ERROR: {e}")


# =================================================
# WATCHDOG
# =================================================
def run_watchdog():

    try:
        w = Watchdog()
        w.run()

    except Exception as e:
        print("[WATCHDOG ERROR]", e)
        telegram.send(f"❌ WATCHDOG ERROR: {e}")


# =================================================
# POSITION SYNC (BYBIT ↔ LOCAL)
# =================================================
def run_sync():

    while True:

        try:
            position_sync.sync()
            time.sleep(10)

        except Exception as e:
            print("[SYNC ERROR]", e)
            telegram.send(f"❌ SYNC ERROR: {e}")


# =================================================
# MAIN
# =================================================
if __name__ == "__main__":

    print("🚀 ====================================")
    print("🚀  FULL TRADING SYSTEM START")
    print("🚀 ====================================")

    telegram.send("🚀 FULL TRADING SYSTEM STARTED")

    # ============================
    # THREAD 1 - MARKET WS
    # ============================
    t1 = threading.Thread(target=run_market_ws, daemon=True)

    # ============================
    # THREAD 2 - FILL WS
    # ============================
    t2 = threading.Thread(target=run_fill_ws, daemon=True)

    # ============================
    # THREAD 3 - HEARTBEAT
    # ============================
    t3 = threading.Thread(target=heartbeat, daemon=True)

    # ============================
    # THREAD 4 - WATCHDOG
    # ============================
    t4 = threading.Thread(target=run_watchdog, daemon=True)

    # ============================
    # THREAD 5 - POSITION SYNC
    # ============================
    t5 = threading.Thread(target=run_sync, daemon=True)

    # START ALL
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    # KEEP ALIVE
    while True:
        time.sleep(1)
