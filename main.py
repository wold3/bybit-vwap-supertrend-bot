import threading
import time

from services.ws_server import start_ws_server
from execution.execution_engine import engine
from strategy.strategy_engine import run_strategy
from watchdog import start_watchdog


# =====================================================
# 🔥 WebSocket 서버 실행
# =====================================================
def start_ws():
    print("[WS] Starting WebSocket server...")
    start_ws_server()


# =====================================================
# 🔥 전략 루프
# =====================================================
def start_strategy():

    print("[STRATEGY] Starting strategy engine...")

    while True:

        try:
            run_strategy(engine)

        except Exception as e:
            print("[STRATEGY ERROR]", e)

        time.sleep(1)


# =====================================================
# 🔥 메인 실행
# =====================================================
def main():

    print("🚀 SYSTEM INIT START")

    # 1. Watchdog
    start_watchdog()
    print("Watchdog started")

    # 2. WebSocket 서버 (백그라운드)
    ws_thread = threading.Thread(target=start_ws, daemon=True)
    ws_thread.start()
    print("WebSocket started")

    # 3. Strategy engine (백그라운드)
    strategy_thread = threading.Thread(target=start_strategy, daemon=True)
    strategy_thread.start()
    print("Strategy started")

    # 4. 상태 루프 (메인 유지)
    print("TRADING SYSTEM RUNNING")

    while True:
        time.sleep(5)


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    main()
