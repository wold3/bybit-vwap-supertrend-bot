import time
import threading

from config import MAX_TRADES_PER_MIN, MAX_DAILY_LOSS, MAX_LOSS_STREAK

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

        if state["trade_count"] >= MAX_TRADES_PER_MIN:
            return False

        state["trade_count"] += 1
        return True


def update_trade_result(pnl):
    with lock:
        state["pnl"] += pnl
        state["balance"] += pnl
        state["equity"].append(state["balance"])

        if pnl < 0:
            state["loss_streak"] += 1
        else:
            state["loss_streak"] = 0


def should_stop():
    with lock:
        if state["pnl"] <= -MAX_DAILY_LOSS:
            return True
        if state["loss_streak"] >= MAX_LOSS_STREAK:
            return True
        return False


def get_status():
    with lock:
        return {
            "balance": state["balance"],
            "pnl": state["pnl"],
            "loss_streak": state["loss_streak"],
            "trade_count": state["trade_count"],
            "equity_latest": state["equity"][-1],
        }


# ==========================
# 🧠 REWARD FUNCTION (NEW)
# ==========================

def compute_reward(pnl):
    if pnl > 0:
        return pnl * 1.2
    return pnl * 1.5
