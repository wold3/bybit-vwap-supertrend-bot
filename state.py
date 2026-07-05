import threading
import time

from execution_model import simulate_execution

lock = threading.Lock()

state = {
    "balance": 1000.0,
    "pnl": 0.0,
    "loss_streak": 0,
    "equity": [1000.0],
}


def compute_real_pnl(entry, exit, qty, volatility):

    entry_exec, entry_cost = simulate_execution(entry, qty, volatility)
    exit_exec, exit_cost = simulate_execution(exit, qty, volatility)

    pnl = (exit_exec - entry_exec) * qty
    pnl -= (entry_cost + exit_cost) * 0.001

    return pnl


def update_trade_result(pnl):

    with lock:

        state["pnl"] += pnl
        state["balance"] += pnl
        state["equity"].append(state["balance"])

        if pnl < 0:
            state["loss_streak"] += 1
        else:
            state["loss_streak"] = 0


def get_status():

    return {
        "balance": state["balance"],
        "pnl": state["pnl"],
        "equity_last": state["equity"][-1],
    }
