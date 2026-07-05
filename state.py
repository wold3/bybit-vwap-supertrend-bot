import time
import threading

from config import MAX_TRADES_PER_MIN, MAX_DAILY_LOSS, MAX_LOSS_STREAK
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


# =====================================================
# TRADE LIMIT
# =====================================================

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


# =====================================================
# REAL PNL SYNC (핵심)
# =====================================================

def sync_real_pnl(symbol):

    pnl = get_unrealized_pnl(symbol)

    with lock:

        state["pnl"] = pnl
        state["balance"] = 1000.0 + pnl
        state["equity"].append(state["balance"])

    return pnl


# =====================================================
# RISK CHECK
# =====================================================

def should_stop():

    with lock:

        if state["pnl"] <= -MAX_DAILY_LOSS:
            return True

        if state["loss_streak"] >= MAX_LOSS_STREAK:
            return True

        return False


# =====================================================
# STATUS
# =====================================================

def get_status():

    with lock:

        return {
            "balance": state["balance"],
            "pnl": state["pnl"],
            "loss_streak": state["loss_streak"],
            "trade_count": state["trade_count"],
            "equity_latest": state["equity"][-1],
            "equity_points": len(state["equity"]),
        }
