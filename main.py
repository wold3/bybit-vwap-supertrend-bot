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
# BYBIT WALLET
# ==============================
from portfolio.bybit_wallet import wallet


# ==============================
# ENV LOAD
# ==============================
load_dotenv()



# =================================================
# ENGINE INIT
# =================================================

execution_engine = BybitExecutionEngine()

strategy_engine = StrategyEngine(
    execution_engine
)



# =================================================
# MARKET WS
# =================================================

def run_market_ws():

    try:

        start_ws(strategy_engine)

    except Exception as e:

        print(
            "[MARKET WS ERROR]",
            e
        )



# =================================================
# FILL WS
# =================================================

def run_fill_ws():

    try:

        start_fill_ws()

    except Exception as e:

        print(
            "[FILL WS ERROR]",
            e
        )



# =================================================
# WATCHDOG
# =================================================

def run_watchdog():

    try:

        watchdog = Watchdog()

        watchdog.run()


    except Exception as e:

        print(
            "[WATCHDOG ERROR]",
            e
        )



# =================================================
# HEARTBEAT
# =================================================

def heartbeat():

    while True:

        print(
            "[HEARTBEAT] SYSTEM OK"
        )

        time.sleep(30)



# =================================================
# BYBIT REAL EQUITY
# =================================================

def get_account_equity():

    try:

        equity = wallet.get_equity()

        return float(equity)


    except Exception as e:

        print(
            "[EQUITY FETCH ERROR]",
            e
        )

        return 0



# =================================================
# EQUITY MONITOR
# =================================================

def run_equity_monitor():

    last_equity = 0


    while True:

        try:

            equity = get_account_equity()


            if equity > 0:


                # Drawdown 계산 업데이트
                drawdown_guard.update(
                    equity
                )


                if equity != last_equity:


                    print(
                        f"[BYBIT EQUITY] {equity}"
                    )


                    last_equity = equity



            time.sleep(5)



        except Exception as e:


            print(
                "[EQUITY LOOP ERROR]",
                e
            )


            time.sleep(5)



# =================================================
# MAIN
# =================================================

if __name__ == "__main__":


    print(
        "===================================="
    )

    print(
        "🚀 BYBIT AUTO TRADING SYSTEM START"
    )

    print(
        "===================================="
    )



    # ------------------------------
    # THREADS
    # ------------------------------

    t1 = threading.Thread(
        target=run_market_ws,
        daemon=True
    )


    t2 = threading.Thread(
        target=run_fill_ws,
        daemon=True
    )


    t3 = threading.Thread(
        target=run_watchdog,
        daemon=True
    )


    t4 = threading.Thread(
        target=heartbeat,
        daemon=True
    )


    t5 = threading.Thread(
        target=run_equity_monitor,
        daemon=True
    )



    # ------------------------------
    # START
    # ------------------------------

    t1.start()

    t2.start()

    t3.start()

    t4.start()

    t5.start()



    # ------------------------------
    # KEEP RUNNING
    # ------------------------------

    while True:

        time.sleep(1)
