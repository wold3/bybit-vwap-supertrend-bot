
import time
import threading
from dotenv import load_dotenv

# ==============================
# CORE ENGINE
# ==============================
from execution.execution_engine import BybitExecutionEngine
from strategy.strategy_engine import StrategyEngine

# ==============================
# SERVICES
# ==============================
from services.ws_client import start_ws
from services.fill_ws import start_fill_ws

# ==============================
# RISK
# ==============================
from risk.drawdown_guard import drawdown_guard

# ==============================
# WATCHDOG
# ==============================
from watchdog import Watchdog

# ==============================
# PORTFOLIO / EQUITY
# ==============================
from portfolio.portfolio_engine import portfolio_engine

# ==============================
# ENV
# ==============================
load_dotenv()


# =================================================
# INIT ENGINE
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


# =================================================
# FILL WS
# =================================================
def run_fill_ws():

    try:
        start_fill_ws()

    except Exception as e:
        print("[FILL WS ERROR]", e)


# =================================================
# WATCHDOG
# =================================================
def run_watchdog():

    try:
        Watchdog().run()

    except Exception as e:
        print("[WATCHDOG ERROR]", e)


# =================================================
# HEARTBEAT
# =================================================
def heartbeat():

    while True:

        print("[HEARTBEAT] SYSTEM OK")

        time.sleep(30)


# =================================================
# EQUITY FETCH
# =================================================
def get_account_equity():

    try:
        return portfolio_engine.get_total_equity()

    except Exception as e:

        print("[EQUITY ERROR]", e)

        return 0


# =================================================
# EQUITY MONITOR (CRITICAL)
# =================================================
def run_equity_monitor():

    last_equity = 0

    while True:

        try:

            equity = get_account_equity()

            if equity > 0:

                drawdown_guard.update(equity)

                if equity != last_equity:

                    print(f"[EQUITY] {equity}")

                    last_equity = equity

            time.sleep(5)

        except Exception as e:

            print("[EQUITY LOOP ERROR]", e)

            time.sleep(5)


# =================================================
# MAIN
# =================================================
if __name__ == "__main__":

    print("🚀 =====================================")
    print("🚀  FULL TRADING SYSTEM STARTING")
    print("🚀 =====================================")

    # ==========================
    # THREAD 1 - MARKET WS
    # ==========================
    t1 = threading.Thread(target=run_market_ws, daemon=True)

    # ==========================
    # THREAD 2 - FILL WS
    # ==========================
    t2 = threading.Thread(target=run_fill_ws, daemon=True)

    # ==========================
    # THREAD 3 - WATCHDOG
    # ==========================
    t3 = threading.Thread(target=run_watchdog, daemon=True)

    # ==========================
    # THREAD 4 - HEARTBEAT
    # ==========================
    t4 = threading.Thread(target=heartbeat, daemon=True)

    # ==========================
    # THREAD 5 - EQUITY MONITOR (핵심)
    # ==========================
    t5 = threading.Thread(target=run_equity_monitor, daemon=True)

    # ==========================
    # START ALL
    # ==========================
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    # ==========================
    # KEEP ALIVE
    # ==========================
    while True:
        time.sleep(1)
