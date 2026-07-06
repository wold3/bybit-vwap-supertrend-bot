import numpy as np
from collections import deque

from risk.risk_engine import risk_engine
from strategy.strategy_router import trend_direction, volatility


# =====================================================
# Memory (시장 학습)
# =====================================================

class TradingBrain:

    def __init__(self):

        self.win_memory = deque(maxlen=200)
        self.strategy_memory = deque(maxlen=200)
        self.pnl_memory = deque(maxlen=200)

    # =====================================================
    # 전략 기록
    # =====================================================

    def record(self, strategy, pnl):

        self.strategy_memory.append(strategy)
        self.pnl_memory.append(pnl)

        self.win_memory.append(1 if pnl > 0 else 0)

    # =====================================================
    # 전략별 성능 계산
    # =====================================================

    def strategy_score(self, strategy):

        if len(self.strategy_memory) < 20:
            return 50

        idx = [i for i, s in enumerate(self.strategy_memory) if s == strategy]

        if not idx:
            return 50

        pnl = [self.pnl_memory[i] for i in idx if i < len(self.pnl_memory)]

        if len(pnl) == 0:
            return 50

        return np.mean(pnl)

    # =====================================================
    # 전체 승률
    # =====================================================

    def win_rate(self):

        if len(self.win_memory) < 10:
            return 50

        return round(sum(self.win_memory) / len(self.win_memory) * 100, 2)

    # =====================================================
    # 최적 전략 선택 (핵심)
    # =====================================================

    def select_strategy(self):

        trend = trend_direction()
        vol = volatility()

        scores = {
            "trend": 0,
            "range": 0,
            "safe": 0
        }

        # -------------------------
        # trend bias
        # -------------------------
        if trend == "TREND_UP" or trend == "TREND_DOWN":
            scores["trend"] += 30
        else:
            scores["range"] += 30

        # -------------------------
        # volatility bias
        # -------------------------
        if vol > 0.02:
            scores["safe"] += 30
        elif vol < 0.01:
            scores["trend"] += 10

        # -------------------------
        # performance memory bias
        # -------------------------
        for s in scores:
            scores[s] += self.strategy_score(s) * 0.1

        best = max(scores, key=scores.get)

        return best, scores

    # =====================================================
    # drawdown recovery mode
    # =====================================================

    def recovery_mode(self):

        status = risk_engine.status()

        if status["drawdown"] > 0.1:
            return True

        if status["win_rate"] < 40:
            return True

        return False

    # =====================================================
    # dynamic risk override
    # =====================================================

    def adjusted_risk(self):

        base = risk_engine.dynamic_risk()

        if self.recovery_mode():
            return base * 0.5  # 보수 모드

        if risk_engine.win_rate() > 60:
            return base * 1.2  # 공격 모드

        return base

    # =====================================================
    # decision engine
    # =====================================================

    def decide(self, signal, price):

        strategy, scores = self.select_strategy()

        recovery = self.recovery_mode()

        return {
            "strategy": strategy,
            "scores": scores,
            "recovery_mode": recovery,
            "risk": self.adjusted_risk(),
            "win_rate": self.win_rate(),
        }


# =====================================================
# Singleton
# =====================================================

brain = TradingBrain()
