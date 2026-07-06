import logging

from strategy.strategy_router import route
from risk.risk_engine import allow_trade
from execution.execution_engine import engine

logger = logging.getLogger(__name__)


# =====================================================
# Strategy Core Executor
# =====================================================
def execute_strategy(
    signal,
    price,
    symbol,
    qty,
):

    # =================================================
    # 1. Risk Check (1차 필터)
    # =================================================
    if not allow_trade():

        logger.warning("Risk engine blocked trade")

        return {
            "success": False,
            "reason": "risk_block",
        }

    # =================================================
    # 2. Strategy Routing (시장 상태 판단)
    # =================================================
    allow, regime = route(signal, price)

    if not allow:

        logger.info("Strategy filtered signal")

        return {
            "success": False,
            "reason": "strategy_filter",
            "regime": regime,
        }

    # =================================================
    # 3. Strategy Mapping
    # =================================================
    if regime == "TREND_UP":
        strategy = "trend"

    elif regime == "RANGE":
        strategy = "range"

    else:
        strategy = "safe"

    # =================================================
    # 4. Execution Call (핵심)
    # =================================================
    order_result = engine.execute(
        signal=signal,
        symbol=symbol,
        qty=qty,
        strategy=strategy,
        regime=regime,
    )

    # =================================================
    # 5. Return Result
    # =================================================
    return {
        "success": order_result.get("success", False),
        "strategy": strategy,
        "regime": regime,
        "signal": signal,
        "order": order_result,
    }


# =====================================================
# Webhook Entry Point
# =====================================================
def execute_signal(data, symbol, qty, price):

    signal = data.get("signal")

    if not signal:
        return {
            "success": False,
            "reason": "no_signal",
        }

    return execute_strategy(
        signal=signal,
        price=price,
        symbol=symbol,
        qty=qty,
    )


# =====================================================
# Utility Functions
# =====================================================
def can_execute(signal, price, symbol, qty):

    result = execute_strategy(
        signal=signal,
        price=price,
        symbol=symbol,
        qty=qty,
    )

    return result.get("success", False)


def get_strategy(signal, price):

    allow, regime = route(signal, price)

    if not allow:
        return None

    if regime == "TREND_UP":
        return "trend"

    if regime == "RANGE":
        return "range"

    return "safe"


def get_regime(signal, price):

    allow, regime = route(signal, price)

    if not allow:
        return "BLOCKED"

    return regime


# =====================================================
# Health Check
# =====================================================
def health():

    return {
        "engine": "strategy_wrapper",
        "status": "active",
    }


# =====================================================
# Export
# =====================================================
__all__ = [
    "execute_strategy",
    "execute_signal",
    "can_execute",
    "get_strategy",
    "get_regime",
    "health",
]
