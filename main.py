import time
import threading
import os

from dotenv import load_dotenv

from services.ws_server import start_ws_server
from strategy.strategy_engine import run_strategy
from execution.execution_engine import engine
from watchdog import start_watchdog


# =====================================================
# 🔥 ENV LOAD
# =====================================================
load_dotenv()


# =====================================================
# 🔥 WEBSOCKET START
# =====================================================
def start_ws():
    print("[WS] Starting WebSocket server...")
    start_ws_server()


# =====================================================
# 🔥 STRATEGY LOOP
# =====================================================
def start_strategy():

    print("[STRATEGY] Engine started")

    while True:

        try:
            run_strategy(engine)

        except Exception as e:
            print("[STRATEGY ERROR]", e)

        time.sleep(1)


# =====================================================
# 🔥 MAIN SYSTEM
# =====================================================
def main():

    print("===================================")
    print("🚀 AUTO TRADING SYSTEM START")
    print("===================================")

    # 1. Watchdog
    start_watchdog()
    print("[OK] Watchdog running")

    # 2. WebSocket server (background)
    ws_thread = threading.Thread(target=start_ws, daemon=True)
    ws_thread.start()
    print("[OK] WebSocket running")

    # 3. Strategy engine (background)
    strategy_thread = threading.Thread(target=start_strategy, daemon=True)
    strategy_thread.start()
    print("[OK] Strategy running")

    # 4. Execution engine ready
    print("[OK] Execution engine ready")

    # 5. Keep alive loop
    print("===================================")
    print("SYSTEM IS LIVE")
    print("===================================")

    while True:
        time.sleep(5)


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    main()
