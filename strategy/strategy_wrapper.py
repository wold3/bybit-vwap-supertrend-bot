import logging

from risk.risk_engine import risk_engine
from execution.execution_engine import execute_order
from strategy_router import route

logger = logging.getLogger(__name__)


# =====================================================
# 신호 품질 필터 (실전 핵심)
# =====================================================

def signal_quality_filter(signal, price):

    # 너무 약한 신호 제거 (노이즈 필터)
    if signal is None:
        return False

    if price is None or price <= 0:
        return False

    return True


# =====================================================
# 전략 매핑
# =====================================================

def map_strategy(regime):

    if regime == "TREND_UP":
        return "trend"

    if regime == "TREND_DOWN":
        return "trend_short"

    if regime == "RANGE":
        return "mean_reversion"

    return "safe"


# =====================================================
# 메인 전략 실행
# =====================================================

def execute_strategy(signal, price, symbol, equity):

    # ----------------------------
    # 1. Risk Check
    # ----------------------------
    if not risk_engine.allow_trade():
        return {
            "success": False,
            "reason": "risk_block",
        }

    # ----------------------------
    # 2. Signal Filter
    # ----------------------------
    if not signal_quality_filter(signal, price):
        return {
            "success": False,
            "reason": "bad_signal",
        }

    # ----------------------------
    # 3. Market Regime
    # ----------------------------
    allow, regime = route(signal, price)

    if not allow:
        return {
            "success": False,
            "reason": "filtered",
            "regime": regime,
        }

    # ----------------------------
    # 4. Strategy 결정
    # ----------------------------
    strategy = map_strategy(regime)

    win_rate = risk_engine.win_rate()
    risk_score = risk_engine.risk_score()

    # ----------------------------
    # 5. 최소 기대값 필터 (실전 핵심)
    # ----------------------------
    if win_rate < 40 and risk_score < 50:
        return {
            "success": False,
            "reason": "low_expectancy",
            "strategy": strategy,
        }

    # ----------------------------
    # 6. Execution
    # ----------------------------
    result = execute_order(
        signal=signal,
        symbol=symbol,
        price=price,
        equity=equity,
        win_rate=win_rate,
    )

    return {
        "success": result.get("success", False),
        "strategy": strategy,
        "regime": regime,
        "execution": result,
    }


# =====================================================
# Helper API
# =====================================================

def can_execute(signal, price):
    return risk_engine.allow_trade() and signal_quality_filter(signal, price)


def get_strategy(signal, price):
    _, regime = route(signal, price)
    return map_strategy(regime)


def get_regime(signal, price):
    _, regime = route(signal, price)
    return regime


def health():

    return {
        "engine": "strategy_wrapper",
        "risk": risk_engine.status(),
        "healthy": True,
    }


# =====================================================
# Export
# =====================================================

__all__ = [
    "execute_strategy",
    "can_execute",
    "get_strategy",
    "get_regime",
    "health",
]
