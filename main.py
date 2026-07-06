import threading

from execution.execution_engine import engine
from strategy.strategy_engine import StrategyEngine
from services.ws_client import start_ws


# =================================================
# INIT
# =================================================
strategy = StrategyEngine(engine)


# =================================================
# RUN WS IN THREAD
# =================================================
def run_ws():

    start_ws(strategy)


# =================================================
# MAIN
# =================================================
if __name__ == "__main__":

    print("🚀 SYSTEM START")

    import telegram
    telegram.telegram.send("🚀 LIVE TRADING STARTED")

    t = threading.Thread(target=run_ws)
    t.start()

    t.join()
