import time
import threading
from bybit_api import get_unrealized_pnl

lock = threading.Lock()

state = {
    "balance": 1000.0,
    "pnl": 0.0,
    "loss_streak": 0,
    "trade_count": 0,
    "last_reset": time.time(),
    "equity": [1000.0],
}


def can_trade():

    with lock:

        now = time.time()

        if now - state["last_reset"] >= 60:
            state["trade_count"] = 0
            state["last_reset"] = now

        if state["trade_count"] >= 3:
            return False

        state["trade_count"] += 1
        return True


def get_real_pnl(symbol):
    return get_unrealized_pnl(symbol)


def compute_reward(pnls: dict):

    total = sum(pnls.values())

    if total > 0:
        return total * 1.2

    return total * 1.5


def update_trade_result(value):

    with lock:

        state["pnl"] += value
        state["balance"] += value
        state["equity"].append(state["balance"])


def get_status():

    with lock:

        return {
            "balance": state["balance"],
            "pnl": state["pnl"],
            "equity_latest": state["equity"][-1],
            "equity_points": len(state["equity"]),
        }
