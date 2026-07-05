from strategy_router import route
from risk_engine import should_stop


def execute_strategy(signal, price):
    """
    전략 실행 Wrapper (최종 의사결정 레이어)
    """

    # ----------------------------
    # 1. Risk Stop Check
    # ----------------------------

    if should_stop():
        return {
            "success": False,
            "reason": "risk_stop",
            "strategy": None,
            "regime": None,
        }

    # ----------------------------
    # 2. Strategy Routing
    # ----------------------------

    allow, regime = route(signal, price)

    # ----------------------------
    # 3. Filter 결과
    # ----------------------------

    if not allow:
        return {
            "success": False,
            "reason": "filtered",
            "strategy": "none",
            "regime": regime,
        }

    # ----------------------------
    # 4. Strategy 결정
    # ----------------------------

    # regime 기반 단순 전략 매핑
    if regime == "TREND_UP":
        strategy = "trend"

    elif regime == "RANGE":
        strategy = "range"

    else:
        strategy = "safe"

    return {
        "success": True,
        "strategy": strategy,
        "regime": regime,
        "signal": signal,
    }


def can_execute(signal, price):
    """
    주문 가능 여부만 반환
    """

    return execute_strategy(signal, price)["success"]


def get_strategy(signal, price):
    """
    선택된 전략 반환
    """

    return execute_strategy(signal, price)["strategy"]


def get_regime(signal, price):
    """
    시장 상태 반환
    """

    return execute_strategy(signal, price)["regime"]
