from ml_filter import should_enter_market
from risk_engine import should_stop
from strategy_wrapper import execute_strategy


def allow_trade(signal, price):
    """
    AI 기반 거래 허용 여부 판단

    Args:
        signal (str): TradingView Signal
        price (float): 현재 가격

    Returns:
        (bool, str)
    """

    # -------------------------
    # Risk Filter
    # -------------------------
    if should_stop():
        return False, "risk_stop"

    # -------------------------
    # ML Filter
    # -------------------------
    allow, score = should_enter_market(price)

    if not allow:
        return False, f"ml_filter ({score})"

    # -------------------------
    # Strategy Filter
    # -------------------------
    result = execute_strategy(
        signal,
        price,
    )

    if not result["success"]:
        return False, result["reason"]

    return True, result["strategy"]


def get_trade_reason(signal, price):
    """
    거래 가능 여부와 이유 반환
    """

    return allow_trade(signal, price)


def is_allowed(signal, price):
    """
    True / False만 반환
    """

    return allow_trade(signal, price)[0]
