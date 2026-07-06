import numpy as np


class Indicators:

    # =====================================================
    # VWAP
    # =====================================================
    def vwap(self, prices, volumes):

        if len(prices) != len(volumes) or len(prices) == 0:
            return None

        pv = np.sum(np.array(prices) * np.array(volumes))
        vol = np.sum(volumes)

        if vol == 0:
            return None

        return pv / vol

    # =====================================================
    # Simple Moving Average
    # =====================================================
    def sma(self, prices, period=20):

        if len(prices) < period:
            return None

        return np.mean(prices[-period:])

    # =====================================================
    # SuperTrend (simplified)
    # =====================================================
    def supertrend(self, prices, period=10, multiplier=3):

        if len(prices) < period:
            return None

        atr = np.mean(np.abs(np.diff(prices[-period:])))
        hl2 = (max(prices[-period:]) + min(prices[-period:])) / 2

        upper_band = hl2 + (multiplier * atr)
        lower_band = hl2 - (multiplier * atr)

        current = prices[-1]

        if current > upper_band:
            return "UP"

        elif current < lower_band:
            return "DOWN"

        else:
            return "NEUTRAL"

    # =====================================================
    # Trend Strength
    # =====================================================
    def trend_strength(self, prices):

        if len(prices) < 30:
            return 0.0

        short = np.mean(prices[-10:])
        long = np.mean(prices[-30:])

        return abs(short - long) / long


# =====================================================
# Singleton
# =====================================================
indicators = Indicators()
