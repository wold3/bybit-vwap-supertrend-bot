import logging

from strategy.signal_parser import parse_signal
from strategy.strategy_router import route
from risk.risk_engine import allow_trade
from execution.execution_engine import engine

logger = logging.getLogger(__name__)


def execute_strategy(data, symbol=None, qty=None, price=None):
    """
    TradingView → 최종 실행까지 연결되는 메인 엔트리
    """

    try:

        # =====================================================
        # 1. Signal Parse
        # =====================================================
        signal = parse_signal(data)

        if not signal:
            return {
                "success": False,
                "reason": "invalid_signal",
            }

        # =====================================================
        # 2. Risk Check (1차 필터)
        # =====================================================
        if not allow_trade():
            return {
                "success": False,
                "reason": "risk_block",
            }

        # =====================================================
        # 3. Market Regime Routing
        # =====================================================
        allow, regime = route(signal, price or 0)

        if not allow:
            return {
                "success": False,
                "reason": "filtered",
                "regime": regime,
            }

        # =====================================================
        # 4. Strategy Mapping
        # =====================================================
        if regime == "TREND_UP":
            strategy = "trend"

        elif regime == "TREND_DOWN":
            strategy = "trend_short"

        elif regime == "RANGE":
            strategy = "mean_reversion"

        else:
            strategy = "safe"

        result = {
            "success": True,
            "signal": signal,
            "strategy": strategy,
            "regime": regime,
        }

        # =====================================================
        # 5. Execution Trigger
        # =====================================================
        if symbol and qty:

            order = engine.execute(
                signal=signal,
                symbol=symbol,
                qty=qty,
                strategy=strategy,
                regime=regime,
            )

            result["order"] = order

        return result

    except Exception as e:
        logger.exception(e)

        return {
            "success": False,
            "reason": str(e),
        }


# =====================================================
# Helper APIs
# =====================================================

def can_execute(data, price=None):
    return execute_strategy(data, price=price).get("success", False)


def get_strategy(data, price=None):
    return execute_strategy(data, price=price).get("strategy")


def get_regime(data, price=None):
    return execute_strategy(data, price=price).get("regime")


def execute_signal(data, symbol, qty, price=None):
    """
    실제 주문 실행 wrapper
    """
    return execute_strategy(
        data=data,
        symbol=symbol,
        qty=qty,
        price=price,
    )
