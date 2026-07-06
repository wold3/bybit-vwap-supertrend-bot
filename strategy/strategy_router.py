import logging

logger = logging.getLogger(__name__)


def route(signal: str, price: float):
    """
    시장 상태 기반 전략 라우팅
    """

    try:
        if price is None:
            return False, "UNKNOWN"

        # =========================
        # 간단한 regime 판단 로직
        # (실전에서는 indicator로 교체 가능)
        # =========================

        if signal in ["BUY", "LONG"]:
            regime = "TREND_UP"
            allow = True

        elif signal in ["SELL", "SHORT"]:
            regime = "TREND_DOWN"
            allow = True

        else:
            regime = "RANGE"
            allow = False

        return allow, regime

    except Exception as e:
        logger.exception(e)
        return False, "ERROR"


# =====================================================
# 추가 유틸
# =====================================================

def is_trend(regime: str) -> bool:
    return regime in ["TREND_UP", "TREND_DOWN"]


def is_range(regime: str) -> bool:
    return regime == "RANGE"


def is_safe(regime: str) -> bool:
    return regime != "ERROR"
