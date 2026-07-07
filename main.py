import time
import threading
from dotenv import load_dotenv


# =====================================
# ENV
# =====================================

load_dotenv()



# =====================================
# CORE ENGINE
# =====================================

from execution.execution_engine import BybitExecutionEngine
from strategy.strategy_engine import StrategyEngine



# =====================================
# SERVICES
# =====================================

from services.ws_client import start_ws
from services.fill_ws import start_fill_ws
from services.private_ws import private_ws



# =====================================
# RISK
# =====================================

from risk.drawdown_guard import drawdown_guard



# =====================================
# WATCHDOG
# =====================================

from watchdog import Watchdog



# =====================================
# BYBIT WALLET
# =====================================

from portfolio.bybit_wallet import wallet




# =====================================
# ENGINE INIT
# =====================================

execution_engine = BybitExecutionEngine()


strategy_engine = StrategyEngine(
    execution_engine
)





# =====================================
# PUBLIC MARKET WS
# =====================================

def run_market_ws():

    try:

        print(
            "📡 PUBLIC WS START"
        )

        start_ws(
            strategy_engine
        )


    except Exception as e:

        print(
            "[PUBLIC WS ERROR]",
            e
        )





# =====================================
# FILL WS
# =====================================

def run_fill_ws():

    try:

        print(
            "📥 FILL WS START"
        )

        start_fill_ws()


    except Exception as e:

        print(
            "[FILL WS ERROR]",
            e
        )





# =====================================
# PRIVATE WS
# =====================================

def run_private_ws():

    try:

        print(
            "🔐 PRIVATE WS START"
        )

        private_ws.start()


    except Exception as e:

        print(
            "[PRIVATE WS ERROR]",
            e
        )





# =====================================
# WATCHDOG
# =====================================

def run_watchdog():

    try:

        print(
            "🐶 WATCHDOG START"
        )

        watchdog = Watchdog()

        watchdog.run()



    except Exception as e:

        print(
            "[WATCHDOG ERROR]",
            e
        )





# =====================================
# HEARTBEAT
# =====================================

def heartbeat():

    while True:

        print(
            "💓 SYSTEM ALIVE"
        )


        time.sleep(30)





# =====================================
# REAL EQUITY
# =====================================

def get_account_equity():

    try:

        equity = wallet.get_equity()

        return float(
            equity
        )


    except Exception as e:

        print(
            "[EQUITY ERROR]",
            e
        )

        return 0





# =====================================
# EQUITY MONITOR
# =====================================

def run_equity_monitor():


    last = 0


    while True:


        try:


            equity = get_account_equity()



            if equity > 0:


                drawdown_guard.update(
                    equity
                )



                if equity != last:


                    print(
                        f"💰 EQUITY : {equity}"
                    )


                    last = equity



            time.sleep(5)




        except Exception as e:


            print(
                "[EQUITY LOOP ERROR]",
                e
            )


            time.sleep(5)





# =====================================
# MAIN
# =====================================

if __name__ == "__main__":



    print(
        """
=====================================
🚀 BYBIT AI TRADING BOT START
=====================================
"""
    )



    threads = [

        threading.Thread(
            target=run_market_ws,
            daemon=True
        ),


        threading.Thread(
            target=run_fill_ws,
            daemon=True
        ),


        threading.Thread(
            target=run_private_ws,
            daemon=True
        ),


        threading.Thread(
            target=run_watchdog,
            daemon=True
        ),


        threading.Thread(
            target=heartbeat,
            daemon=True
        ),


        threading.Thread(
            target=run_equity_monitor,
            daemon=True
        )

    ]



    for t in threads:

        t.start()



    print(
        "✅ ALL SERVICES RUNNING"
    )



    # =================================
    # KEEP PROCESS
    # =================================

    while True:

        time.sleep(1)
