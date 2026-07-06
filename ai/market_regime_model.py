import numpy as np


class MarketRegimeModel:

    def __init__(self):

        self.window = 20

    # =====================================================
    # Regime Detection
    # =====================================================
    def predict(self, candles):

        """
        candles: [{'open':, 'high':, 'low':, 'close':}]
        """

        if len(candles) < self.window:
            return "UNKNOWN"

        closes = np.array([c["close"] for c in candles])
        highs = np.array([c["high"] for c in candles])
        lows = np.array([c["low"] for c in candles])

        returns = np.diff(closes)

        volatility = np.std(returns)

        trend = (closes[-1] - closes[0]) / closes[0]

        range_width = np.mean(highs - lows)

        # =================================================
        # Rule-based AI classifier
        # =================================================

        if volatility > 0.015:
            return "VOLATILE"

        if trend > 0.01:
            return "TREND_UP"

        if trend < -0.01:
            return "TREND_DOWN"

        if range_width < np.mean(closes) * 0.002:
            return "RANGE"

        return "MIXED"


# =====================================================
# Singleton
# =====================================================
market_regime_model = MarketRegimeModel()
