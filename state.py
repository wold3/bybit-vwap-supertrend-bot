import time
import threading

from config import (
    MAX_TRADES_PER_MIN,
    MAX_DAILY_LOSS,
    MAX_LOSS_STREAK,
)


# =====================================================
# Thread Lock (안전성)
# =====================================================

lock = threading.Lock()


# =====================================================
# Runtime State
# =====================================================

state = {
    "pnl": 0.0,
    "loss_streak": 0,
    "trade_count": 0,
    "last_reset": time.time(),
}


# =====================================================
# Rate Limiter
# =====================================================

def can_trade():
    """
    1분당 최대 거래 제한
    """

    with lock:

        now = time.time()

        # 1분 리셋
        if now - state["last_reset"] >= 60:
            state["trade_count"] = 0
            state["last_reset"] = now

        if state["trade_count"] >= MAX_TRADES_PER_MIN:
            return False

        state["trade_count"] += 1

        return True


# =====================================================
# PnL Update
# =====================================================

def update_pnl(pnl):
    """
    손익 업데이트
    """

    with lock:

        pnl = float(pnl)

        state["pnl"] += pnl

        if pnl < 0:
            state["loss_streak"] += 1
        else:
            state["loss_streak"] = 0


# =====================================================
# Risk Check
# =====================================================

def should_stop():
    """
    리스크 중단 조건
    """

    with lock:

        if state["pnl"] <= -MAX_DAILY_LOSS:
            return True

        if state["loss_streak"] >= MAX_LOSS_STREAK:
            return True

        return False


# =====================================================
# Reset
# =====================================================

def reset():
    """
    상태 초기화
    """

    with lock:

        state["pnl"] = 0.0
        state["loss_streak"] = 0
        state["trade_count"] = 0
        state["last_reset"] = time.time()


# =====================================================
# Status
# =====================================================

def get_status():
    """
    현재 상태 조회
    """

    with lock:

        return {
            "pnl": state["pnl"],
            "loss_streak": state["loss_streak"],
            "trade_count": state["trade_count"],
            "max_trades_per_min": MAX_TRADES_PER_MIN,
            "daily_loss_limit": MAX_DAILY_LOSS,
            "max_loss_streak": MAX_LOSS_STREAK,
            "seconds_since_reset": round(
                time.time() - state["last_reset"],
                2,
            ),
        }
