import time
import threading

from config import MAX_TRADES_PER_MIN, MAX_DAILY_LOSS, MAX_LOSS_STREAK

# =====================================================
# THREAD SAFE LOCK
# =====================================================

lock = threading.Lock()

# =====================================================
# STATE
# =====================================================

state = {
    "balance": 1000.0,
    "pnl": 0.0,
    "loss_streak": 0,
    "trade_count": 0,
    "last_reset": time.time(),
    "equity": [1000.0],   # equity curve
}


# =====================================================
# TRADE LIMIT (1 MIN RULE)
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
# PnL UPDATE (REAL EQUITY ENGINE)
# =====================================================

def update_trade_result(pnl: float):
    """
    실전 기준: 거래 결과 반영 (PnL → balance → equity curve)
    """

    with lock:

        pnl = float(pnl)

        state["pnl"] += pnl
        state["balance"] += pnl
        state["equity"].append(state["balance"])

        if pnl < 0:
            state["loss_streak"] += 1
        else:
            state["loss_streak"] = 0


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
# STATUS API
# =====================================================

def get_status():

    with lock:

        return {
            "balance": state["balance"],
            "pnl": state["pnl"],
            "loss_streak": state["loss_streak"],
            "trade_count": state["trade_count"],
            "max_trades_per_min": MAX_TRADES_PER_MIN,
            "max_daily_loss": MAX_DAILY_LOSS,
            "max_loss_streak": MAX_LOSS_STREAK,
            "equity_latest": state["equity"][-1],
            "equity_points": len(state["equity"]),
            "seconds_since_reset": round(time.time() - state["last_reset"], 2),
        }


# =====================================================
# EQUITY CURVE API
# =====================================================

def get_equity_curve():

    with lock:
        return state["equity"]


# =====================================================
# RESET (optional)
# =====================================================

def reset():

    with lock:

        state["balance"] = 1000.0
        state["pnl"] = 0.0
        state["loss_streak"] = 0
        state["trade_count"] = 0
        state["last_reset"] = time.time()
        state["equity"] = [1000.0]
