import numpy as np


class TradeFilters:

    def __init__(self):

        self.volatility_window = 20

    # =====================================================
    # Volatility Filter
    # =====================================================
    def volatility_filter(self, prices):

        if len(prices) < self.volatility_window:
            return True

        returns = np.diff(prices)

        vol = np.std(returns)

        return vol > 0.0005

    # =====================================================
    # Momentum Filter
    # =====================================================
    def momentum_filter(self, prices):

        if len(prices) < 10:
            return True

        return prices[-1] > np.mean(prices[-10:])

    # =====================================================
    # Trend Strength Filter
    # =====================================================
    def trend_filter(self, prices):

        if len(prices) < 30:
            return True

        short_ma = np.mean(prices[-10:])
        long_ma = np.mean(prices[-30:])

        return abs(short_ma - long_ma) > 0.001

    # =====================================================
    # Final Decision
    # =====================================================
    def allow_trade(self, prices):

        return (
            self.volatility_filter(prices)
            and self.momentum_filter(prices)
            and self.trend_filter(prices)
        )


# =====================================================
# Singleton
# =====================================================
trade_filters = TradeFilters()


def allow_trade_by_filter(prices):
    return trade_filters.allow_trade(prices)
