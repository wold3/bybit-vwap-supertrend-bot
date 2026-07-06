import logging

from risk.risk_engine import allow_trade
from strategy.strategy_router import route
from execution.execution_engine import engine

logger = logging.getLogger(__name__)


def execute_strategy(signal, price, symbol=None, qty=None):

    # 1. Risk Check
    if not allow_trade():
        return {
            "success": False,
            "reason": "risk_block",
        }

    # 2. Market regime
    allow, regime = route(signal, price)

    if not allow:
        return {
            "success": False,
            "reason": "market_filter",
            "regime": regime,
        }

    # 3. Strategy mapping
    if regime == "TREND_UP":
        strategy = "trend"
    elif regime == "RANGE":
        strategy = "range"
    else:
        strategy = "safe"

    result = {
        "success": True,
        "strategy": strategy,
        "regime": regime,
        "signal": signal,
    }

    # 4. Execution
    if symbol and qty:

        logger.info("EXECUTE %s %s", signal, symbol)

        order = engine.execute(
            signal=signal,
            symbol=symbol,
            qty=qty,
            strategy=strategy,
            regime=regime,
        )

        result["order"] = order

    return result


def can_execute(signal, price):
    return execute_strategy(signal, price)["success"]


def get_strategy(signal, price):
    return execute_strategy(signal, price).get("strategy")


def get_regime(signal, price):
    return execute_strategy(signal, price).get("regime")
