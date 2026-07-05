from config import (
    MAX_DAILY_LOSS,
    MAX_LOSS_STREAK,
)

# ==========================
# Risk State
# ==========================

state = {
    "pnl": 0.0,
    "loss_streak": 0,
    "trade_count": 0,
}


def update_pnl(pnl):
    """
    손익(PnL) 업데이트
    """

    pnl = float(pnl)

    state["pnl"] += pnl
    state["trade_count"] += 1

    if pnl < 0:
        state["loss_streak"] += 1
    else:
        state["loss_streak"] = 0


def should_stop():
    """
    리스크 한도 초과 여부
    """

    if state["pnl"] <= -MAX_DAILY_LOSS:
        return True

    if state["loss_streak"] >= MAX_LOSS_STREAK:
        return True

    return False


def reset():
    """
    리스크 상태 초기화
    """

    state["pnl"] = 0.0
    state["loss_streak"] = 0
    state["trade_count"] = 0


def get_status():
    """
    현재 리스크 상태 반환
    """

    return {
        "pnl": round(state["pnl"], 2),
        "loss_streak": state["loss_streak"],
        "trade_count": state["trade_count"],
        "max_daily_loss": MAX_DAILY_LOSS,
        "max_loss_streak": MAX_LOSS_STREAK,
        "should_stop": should_stop(),
    }


def can_open_position():
    """
    신규 포지션 진입 가능 여부
    """

    return not should_stop()
