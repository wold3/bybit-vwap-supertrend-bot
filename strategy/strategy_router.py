from strategy.indicators import indicators
from strategy.filters import allow_trade_by_filter


class StrategyRouter:

    # =====================================================
    # Main Decision
    # =====================================================
    def route(self, signal, prices, volumes=None):

        # -----------------------------
        # 1. 기본 필터 체크
        # -----------------------------
        if not allow_trade_by_filter(prices):
            return False, "FILTERED"

        # -----------------------------
        # 2. 지표 계산
        # -----------------------------
        vwap = None
        if volumes:
            vwap = indicators.vwap(prices, volumes)

        trend = indicators.supertrend(prices)
        strength = indicators.trend_strength(prices)

        # -----------------------------
        # 3. 약한 시장 제거
        # -----------------------------
        if strength < 0.0005:
            return False, "WEAK_MARKET"

        # -----------------------------
        # 4. SuperTrend 기반 방향 필터
        # -----------------------------
        if trend == "UP" and signal != "BUY":
            return False, "TREND_CONFLICT"

        if trend == "DOWN" and signal != "SELL":
            return False, "TREND_CONFLICT"

        # -----------------------------
        # 5. VWAP 필터 (기관 기준)
        # -----------------------------
        if vwap:

            last_price = prices[-1]

            if signal == "BUY" and last_price < vwap:
                return False, "VWAP_BEARISH"

            if signal == "SELL" and last_price > vwap:
                return False, "VWAP_BULLISH"

        # -----------------------------
        # 6. 통과
        # -----------------------------
        if trend == "UP":
            regime = "TREND_UP"

        elif trend == "DOWN":
            regime = "TREND_DOWN"

        else:
            regime = "RANGE"

        return True, regime


# =====================================================
# Singleton
# =====================================================
router = StrategyRouter()


# =====================================================
# Public API
# =====================================================
def route(signal, prices, volumes=None):
    return router.route(signal, prices, volumes)
