import numpy as np
from collections import deque

from strategy.strategy_router import trend_direction, volatility
from risk.risk_engine import risk_engine


class TradingBrain:

    def __init__(self):

        self.pnl_memory = deque(maxlen=200)
        self.strategy_memory = deque(maxlen=200)
        self.win_memory = deque(maxlen=200)

    # =====================================================
    # 기록
    # =====================================================

    def record(self, strategy, pnl):

        self.strategy_memory.append(strategy)
        self.pnl_memory.append(pnl)
        self.win_memory.append(1 if pnl > 0 else 0)

    # =====================================================
    # 승률
    # =====================================================

    def win_rate(self):

        if len(self.win_memory) < 10:
            return 50.0

        return round(
            sum(self.win_memory) / len(self.win_memory) * 100,
            2
        )

    # =====================================================
    # 전략 점수
    # =====================================================

    def strategy_score(self, strategy):

        idx = [
            i for i, s in enumerate(self.strategy_memory)
            if s == strategy
        ]

        if not idx:
            return 50

        pnl = [self.pnl_memory[i] for i in idx if i < len(self.pnl_memory)]

        if not pnl:
            return 50

        return float(np.mean(pnl))

    # =====================================================
    # 전략 선택 (핵심 AI)
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
        if trend in ["TREND_UP", "TREND_DOWN"]:
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
        # learning bias
        # -------------------------
        for k in scores.keys():
            scores[k] += self.strategy_score(k) * 0.1

        best = max(scores, key=scores.get)

        return best, scores

    # =====================================================
    # 회복 모드
    # =====================================================

    def recovery_mode(self):

        status = risk_engine.status()

        if status["drawdown"] > 0.1:
            return True

        if status["win_rate"] < 40:
            return True

        if status["risk_score"] < 30:
            return True

        return False

    # =====================================================
    # 리스크 보정
    # =====================================================

    def adjusted_risk(self):

        base = risk_engine.dynamic_risk()

        if self.recovery_mode():
            return base * 0.5

        if self.win_rate() > 60:
            return base * 1.2

        return base

    # =====================================================
    # 의사결정
    # =====================================================

    def decide(self, signal, price):

        strategy, scores = self.select_strategy()

        return {
            "strategy": strategy,
            "scores": scores,
            "win_rate": self.win_rate(),
            "recovery": self.recovery_mode(),
            "risk": self.adjusted_risk()
        }


# =====================================================
# SINGLETON
# =====================================================

brain = TradingBrain()
