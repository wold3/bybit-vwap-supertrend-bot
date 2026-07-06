import threading
import time
import os

from dotenv import load_dotenv

from execution.execution_engine import BybitExecutionEngine
from strategy.strategy_engine import StrategyEngine

from services.ws_client import start_ws
from services.fill_ws import start_fill_ws

from telegram import telegram


# =================================================
# ENV LOAD
# =================================================
load_dotenv()


# =================================================
# INIT CORE ENGINE
# =================================================
execution_engine = BybitExecutionEngine()
strategy_engine = StrategyEngine(execution_engine)


# =================================================
# MARKET WS THREAD (PRICE STREAM)
# =================================================
def run_market_ws():

    try:
        start_ws(strategy_engine)
    except Exception as e:
        print("[MARKET WS ERROR]", e)
        telegram.send(f"❌ MARKET WS ERROR: {e}")


# =================================================
# FILL WS THREAD (EXECUTION TRACKING)
# =================================================
def run_fill_ws():

    try:
        start_fill_ws()
    except Exception as e:
        print("[FILL WS ERROR]", e)
        telegram.send(f"❌ FILL WS ERROR: {e}")


# =================================================
# HEARTBEAT (SYSTEM MONITOR)
# =================================================
def heartbeat():

    while True:

        try:
            time.sleep(30)

            print("[HEARTBEAT] SYSTEM ALIVE")

        except Exception as e:

            print("[HEARTBEAT ERROR]", e)
            telegram.send(f"❌ HEARTBEAT ERROR: {e}")


# =================================================
# MAIN START
# =================================================
if __name__ == "__main__":

    print("🚀 ===============================")
    print("🚀 TRADING SYSTEM STARTING")
    print("🚀 ===============================")

    telegram.send("🚀 TRADING SYSTEM STARTED")

    # -------------------------------
    # THREAD 1: MARKET DATA WS
    # -------------------------------
    t1 = threading.Thread(
        target=run_market_ws,
        daemon=True
    )

    # -------------------------------
    # THREAD 2: FILL TRACKER WS
    # -------------------------------
    t2 = threading.Thread(
        target=run_fill_ws,
        daemon=True
    )

    # -------------------------------
    # THREAD 3: HEARTBEAT
    # -------------------------------
    t3 = threading.Thread(
        target=heartbeat,
        daemon=True
    )

    # START ALL
    t1.start()
    t2.start()
    t3.start()

    # KEEP MAIN ALIVE
    while True:
        time.sleep(1)
