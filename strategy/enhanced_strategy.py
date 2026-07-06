import numpy as np

from strategy.indicators import indicators
from strategy.filters import allow_trade_by_filter


class EnhancedStrategy:

    # =====================================================
    # ATR 계산
    # =====================================================
    def atr(self, prices, period=14):

        if len(prices) < period:
            return None

        diffs = np.abs(np.diff(prices[-period:]))

        return np.mean(diffs)

    # =====================================================
    # Entry Signal 강화
    # =====================================================
    def entry_signal(self, signal, prices, volumes=None):

        if not allow_trade_by_filter(prices):
            return False, "FILTER_BLOCK"

        vwap = None

        if volumes:
            vwap = indicators.vwap(prices, volumes)

        trend = indicators.supertrend(prices)
        strength = indicators.trend_strength(prices)

        if strength < 0.001:
            return False, "WEAK_TREND"

        last_price = prices[-1]

        # VWAP filter
        if vwap:

            if signal == "BUY" and last_price < vwap:
                return False, "BELOW_VWAP"

            if signal == "SELL" and last_price > vwap:
                return False, "ABOVE_VWAP"

        # Trend confirmation
        if trend == "UP" and signal != "BUY":
            return False, "TREND_MISMATCH"

        if trend == "DOWN" and signal != "SELL":
            return False, "TREND_MISMATCH"

        return True, "OK"

    # =====================================================
    # Exit Signal (TP/SL + Trailing)
    # =====================================================
    def exit_signal(self, entry_price, current_price, prices, side):

        atr = self.atr(prices)

        if atr is None:
            return None

        tp = atr * 2.5
        sl = atr * 1.5
        trail = atr * 1.0

        # Stop Loss
        if side == "BUY":

            if current_price <= entry_price - sl:
                return "STOP_LOSS"

            if current_price >= entry_price + tp:
                return "TAKE_PROFIT"

            if current_price <= current_price - trail:
                return "TRAIL_EXIT"

        if side == "SELL":

            if current_price >= entry_price + sl:
                return "STOP_LOSS"

            if current_price <= entry_price - tp:
                return "TAKE_PROFIT"

            if current_price >= current_price + trail:
                return "TRAIL_EXIT"

        return None

    # =====================================================
    # Full Strategy Decision
    # =====================================================
    def run(self, signal, prices, volumes=None):

        entry_ok, reason = self.entry_signal(signal, prices, volumes)

        return {
            "entry_allowed": entry_ok,
            "reason": reason,
            "trend": indicators.supertrend(prices),
            "vwap": indicators.vwap(prices, volumes) if volumes else None,
        }


# =====================================================
# Singleton
# =====================================================
enhanced_strategy = EnhancedStrategy()


# =====================================================
# Public API
# =====================================================
def run_strategy(signal, prices, volumes=None):
    return enhanced_strategy.run(signal, prices, volumes)
