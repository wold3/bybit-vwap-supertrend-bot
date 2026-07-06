import numpy as np
from datetime import datetime

from config import MAX_DAILY_LOSS, MAX_LOSS_STREAK


class RiskEngine:

    def __init__(self):

        self.pnl_history = []

        self.daily_pnl = 0.0
        self.trade_count = 0
        self.loss_streak = 0

        self.equity_curve = []

        self.max_drawdown = 0.0
        self.peak_equity = 0.0

        self.base_risk = 0.02

        self.last_reset = datetime.utcnow().date()

    # =====================================================
    # Equity 업데이트 (핵심)
    # =====================================================

    def update_equity(self, pnl):

        self.equity_curve.append(pnl)

        equity = sum(self.equity_curve)

        if equity > self.peak_equity:
            self.peak_equity = equity

        drawdown = self.peak_equity - equity

        if drawdown > self.max_drawdown:
            self.max_drawdown = drawdown

    # =====================================================
    # PnL 업데이트
    # =====================================================

    def update(self, pnl, price=None, qty=None):

        pnl = float(pnl)

        self.pnl_history.append(pnl)

        self.daily_pnl += pnl
        self.trade_count += 1

        self.update_equity(pnl)

        if pnl < 0:
            self.loss_streak += 1
        else:
            self.loss_streak = 0

        if len(self.pnl_history) > 1000:
            self.pnl_history.pop(0)

    # =====================================================
    # Dynamic Risk Scaling (핵심 수익 엔진)
    # =====================================================

    def dynamic_risk(self):

        if self.peak_equity <= 0:
            return self.base_risk

        drawdown_ratio = self.max_drawdown / (self.peak_equity + 1e-9)

        risk = self.base_risk

        # 드로우다운 심하면 축소
        if drawdown_ratio > 0.2:
            risk *= 0.3
        elif drawdown_ratio > 0.1:
            risk *= 0.6
        elif drawdown_ratio > 0.05:
            risk *= 0.8

        # 회복 구간에서는 공격 증가
        if self.daily_pnl > 0:
            risk *= 1.2

        return round(min(risk, 0.05), 4)

    # =====================================================
    # CVaR (tail risk)
    # =====================================================

    def cvar(self):

        if len(self.pnl_history) < 20:
            return 0.0

        arr = np.array(self.pnl_history)

        var = np.percentile(arr, 5)
        tail = arr[arr <= var]

        return float(tail.mean()) if len(tail) else 0.0

    # =====================================================
    # Win Rate
    # =====================================================

    def win_rate(self):

        if len(self.pnl_history) < 10:
            return 0.0

        wins = len([x for x in self.pnl_history if x > 0])

        return round((wins / len(self.pnl_history)) * 100, 2)

    # =====================================================
    # Daily Loss 제한
    # =====================================================

    def exceeded_daily_loss(self):

        return self.daily_pnl <= -abs(MAX_DAILY_LOSS)

    # =====================================================
    # Loss Streak 제한
    # =====================================================

    def exceeded_loss_streak(self):

        return self.loss_streak >= MAX_LOSS_STREAK

    # =====================================================
    # 핵심 판단
    # =====================================================

    def allow_trade(self):

        if self.exceeded_daily_loss():
            return False

        if self.exceeded_loss_streak():
            return False

        # drawdown 보호
        if self.max_drawdown > self.peak_equity * 0.25:
            return False

        return True

    # =====================================================
    # Risk Score
    # =====================================================

    def risk_score(self):

        score = 100.0

        score -= min(abs(self.daily_pnl), 40)
        score -= self.loss_streak * 7

        # drawdown penalty
        if self.max_drawdown > 0:
            score -= self.max_drawdown * 2

        return max(round(score, 2), 0.0)

    # =====================================================
    # 전략 추천 신호 (핵심 추가)
    # =====================================================

    def regime_bias(self):

        if self.win_rate() < 40:
            return "SAFE"

        if self.max_drawdown > 0.1:
            return "CONSERVATIVE"

        if self.daily_pnl > 0:
            return "AGGRESSIVE"

        return "NORMAL"

    # =====================================================
    # 상태
    # =====================================================

    def status(self):

        return {
            "daily_pnl": round(self.daily_pnl, 4),
            "trade_count": self.trade_count,
            "loss_streak": self.loss_streak,
            "win_rate": self.win_rate(),
            "risk_score": self.risk_score(),
            "allow_trade": self.allow_trade(),
            "cvar": round(self.cvar(), 6),
            "drawdown": round(self.max_drawdown, 4),
            "risk": round(self.dynamic_risk(), 4),
            "regime_bias": self.regime_bias(),
        }


# =====================================================
# Singleton
# =====================================================

risk_engine = RiskEngine()


def allow_trade():
    return risk_engine.allow_trade()


def update_risk(pnl, price=None, qty=None):
    risk_engine.update(pnl, price, qty)


def get_risk_status():
    return risk_engine.status()

def should_stop():
    return not risk_engine.allow_trade()


def reset_risk():
    risk_engine.__init__()
