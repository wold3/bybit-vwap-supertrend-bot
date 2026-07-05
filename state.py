import time

from config import (
    MAX_TRADES_PER_MIN,
    MAX_DAILY_LOSS,
    MAX_LOSS_STREAK,
)

# ==========================
# Trade Rate Limiter
# ==========================

trade_count = 0
last_reset = time.time()

# ==========================
# Trading State
# ==========================

state = {
    "pnl": 0.0,
    "loss_streak": 0,
    "trade_count": 0,
}


def can_trade():
    """
    1분당 최대 거래 횟수 제한
    """
    global trade_count, last_reset

    now = time.time()

    if now - last_reset >= 60:
        trade_count = 0
        last_reset = now

    if trade_count >= MAX_TRADES_PER_MIN:
        return False

    trade_count += 1
    state["trade_count"] = trade_count

    return True


def update_pnl(pnl):
    """
    손익 업데이트
    """
    state["pnl"] += float(pnl)

    if pnl < 0:
        state["loss_streak"] += 1
    else:
        state["loss_streak"] = 0


def should_stop():
    """
    리스크 제한 확인
    """

    if state["pnl"] <= -MAX_DAILY_LOSS:
        return True

    if state["loss_streak"] >= MAX_LOSS_STREAK:
        return True

    return False


def reset():
    """
    상태 초기화
    """
    global trade_count, last_reset

    trade_count = 0
    last_reset = time.time()

    state["pnl"] = 0.0
    state["loss_streak"] = 0
    state["trade_count"] = 0


def get_status():
    """
    현재 상태 조회
    """
    return {
        "pnl": state["pnl"],
        "loss_streak": state["loss_streak"],
        "trade_count": trade_count,
        "max_trades_per_min": MAX_TRADES_PER_MIN,
        "daily_loss_limit": MAX_DAILY_LOSS,
        "max_loss_streak": MAX_LOSS_STREAK,
        "seconds_since_reset": round(time.time() - last_reset, 2),
    }
