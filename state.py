import time

from config import MAX_TRADES_PER_MIN

# ==========================
# Trade Rate Limiter
# ==========================

trade_count = 0
last_reset = time.time()


def can_trade():
    """
    1분 동안 최대 거래 횟수 제한
    """

    global trade_count, last_reset

    now = time.time()

    # 60초마다 카운터 초기화
    if now - last_reset >= 60:
        trade_count = 0
        last_reset = now

    if trade_count >= MAX_TRADES_PER_MIN:
        return False

    trade_count += 1
    return True


def reset_trade_counter():
    """
    거래 카운터 강제 초기화
    """

    global trade_count, last_reset

    trade_count = 0
    last_reset = time.time()


def get_trade_count():
    """
    현재 1분 거래 횟수 반환
    """

    return trade_count


def get_status():
    """
    현재 상태 반환
    """

    return {
        "trade_count": trade_count,
        "max_trade_per_min": MAX_TRADES_PER_MIN,
        "seconds_since_reset": round(time.time() - last_reset, 2),
    }
