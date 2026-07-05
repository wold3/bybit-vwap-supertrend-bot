from strategy_router import route
from risk_engine import should_stop


def execute_strategy(signal, price):
    """
    전략 실행 Wrapper

    Args:
        signal (str): TradingView Signal
        price (float): 현재 가격

    Returns:
        dict
    """

    # 리스크 체크
    if should_stop():
        return {
            "success": False,
            "reason": "risk_stop",
            "strategy": None,
            "regime": None,
        }

    # 전략 선택
    result = route(signal, price)

    if not result["allow"]:
        return {
            "success": False,
            "reason": "filtered",
            "strategy": result["strategy"],
            "regime": result["regime"],
        }

    return {
        "success": True,
        "strategy": result["strategy"],
        "regime": result["regime"],
        "signal": signal,
    }


def can_execute(signal, price):
    """
    주문 가능 여부만 반환
    """

    return execute_strategy(signal, price)["success"]


def get_strategy(signal, price):
    """
    선택된 전략명 반환
    """

    result = execute_strategy(signal, price)

    return result["strategy"]


def get_regime(signal, price):
    """
    현재 시장 상태 반환
    """

    result = execute_strategy(signal, price)

    return result["regime"]
