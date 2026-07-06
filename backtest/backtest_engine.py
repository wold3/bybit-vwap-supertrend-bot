import numpy as np
import pandas as pd

from ai.trading_brain import brain
from risk.risk_engine import risk_engine


class BacktestEngine:

    def __init__(self, initial_balance=1000):

        self.initial_balance = initial_balance
        self.balance = initial_balance

        self.equity_curve = []
        self.trades = []

    # =====================================================
    # 시뮬레이션 1트레이드
    # =====================================================

    def simulate_trade(self, price, signal, strategy):

        pnl = np.random.normal(0.5, 2.0)

        self.balance += pnl

        self.equity_curve.append(self.balance)

        self.trades.append({
            "price": price,
            "signal": signal,
            "strategy": strategy,
            "pnl": pnl,
            "balance": self.balance
        })

        brain.record(strategy, pnl)

        return pnl

    # =====================================================
    # 최대 낙폭 (MDD)
    # =====================================================

    def max_drawdown(self):

        peak = -np.inf
        max_dd = 0

        for value in self.equity_curve:

            if value > peak:
                peak = value

            dd = peak - value

            if dd > max_dd:
                max_dd = dd

        return max_dd

    # =====================================================
    # 승률
    # =====================================================

    def win_rate(self):

        wins = len([t for t in self.trades if t["pnl"] > 0])

        if not self.trades:
            return 0

        return wins / len(self.trades) * 100

    # =====================================================
    # 총 수익
    # =====================================================

    def total_return(self):

        return self.balance - self.initial_balance

    # =====================================================
    # 실행
    # =====================================================

    def run(self, prices):

        for price in prices:

            strategy = brain.select_strategy()[0]

            pnl = self.simulate_trade(
                price=price,
                signal="auto",
                strategy=strategy
            )

        return {
            "initial": self.initial_balance,
            "final": self.balance,
            "return": self.total_return(),
            "win_rate": self.win_rate(),
            "max_drawdown": self.max_drawdown(),
            "trades": len(self.trades)
        }


# =====================================================
# 실행 테스트 (예시)
# =====================================================

if __name__ == "__main__":

    engine = BacktestEngine()

    prices = np.random.normal(65000, 100, 200)

    result = engine.run(prices)

    print("BACKTEST RESULT")
    print(result)
