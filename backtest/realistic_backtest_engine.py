import numpy as np
from collections import deque

from ai.trading_brain import brain
from config import FEE_RATE, SLIPPAGE_BUFFER


class RealisticBacktestEngine:

    def __init__(self, initial_balance=1000):

        self.initial_balance = initial_balance
        self.balance = initial_balance

        self.equity_curve = []
        self.trades = deque()

    # =====================================================
    # 체결 가격 계산 (슬리피지 포함)
    # =====================================================

    def execute_price(self, price, side):

        slippage = price * SLIPPAGE_BUFFER

        if side == "BUY":
            return price + slippage
        else:
            return price - slippage

    # =====================================================
    # 수수료 계산
    # =====================================================

    def fee(self, notional):

        return notional * FEE_RATE

    # =====================================================
    # 트레이드 실행
    # =====================================================

    def simulate_trade(self, price, strategy):

        side = "BUY" if np.random.rand() > 0.5 else "SELL"

        entry_price = self.execute_price(price, side)

        # exit price simulation
        exit_price = price + np.random.normal(0, 1.5)

        exit_price = self.execute_price(exit_price, side)

        qty = self.balance * 0.02

        notional = qty * entry_price

        fee = self.fee(notional)

        if side == "BUY":
            pnl = (exit_price - entry_price) * qty
        else:
            pnl = (entry_price - exit_price) * qty

        pnl -= fee

        self.balance += pnl

        self.equity_curve.append(self.balance)

        self.trades.append({
            "strategy": strategy,
            "side": side,
            "entry": entry_price,
            "exit": exit_price,
            "pnl": pnl,
            "balance": self.balance
        })

        brain.record(strategy, pnl)

        return pnl

    # =====================================================
    # MDD
    # =====================================================

    def max_drawdown(self):

        peak = -np.inf
        max_dd = 0

        for v in self.equity_curve:

            if v > peak:
                peak = v

            dd = peak - v

            if dd > max_dd:
                max_dd = dd

        return max_dd

    # =====================================================
    # 승률
    # =====================================================

    def win_rate(self):

        if not self.trades:
            return 0

        wins = len([t for t in self.trades if t["pnl"] > 0])

        return wins / len(self.trades) * 100

    # =====================================================
    # 실행
    # =====================================================

    def run(self, prices):

        for price in prices:

            strategy = brain.select_strategy()[0]

            self.simulate_trade(price, strategy)

        return {
            "initial": self.initial_balance,
            "final": self.balance,
            "return": self.balance - self.initial_balance,
            "win_rate": self.win_rate(),
            "max_drawdown": self.max_drawdown(),
            "trades": len(self.trades)
        }


# =====================================================
# TEST RUN
# =====================================================

if __name__ == "__main__":

    engine = RealisticBacktestEngine()

    prices = np.random.normal(65000, 100, 300)

    result = engine.run(prices)

    print("REALISTIC BACKTEST RESULT")
    print(result)
