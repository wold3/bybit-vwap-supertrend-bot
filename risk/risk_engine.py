import numpy as np
import logging
from datetime import datetime

from config import MAX_DAILY_LOSS, MAX_LOSS_STREAK

logger = logging.getLogger(__name__)


class RiskEngine:

    def __init__(self):

        self.pnl_history = []

        self.daily_pnl = 0.0
        self.trade_count = 0
        self.loss_streak = 0

        self.fee_rate = 0.0006  # Bybit 실수수료 기준 (taker)
        self.slippage_buffer = 0.0003  # 슬리피지 보정
        self.win_rate_filter = 45.0  # 최소 승률 기준(%)

        self.last_reset = datetime.utcnow().date()

    # =====================================================
    # 핵심 PnL 보정 (실전용)
    # =====================================================

    def apply_cost(self, pnl, price=None, qty=None):

        fee = 0.0

        if price and qty:
            fee = price * qty * self.fee_rate * 2  # 진입+청산

        slippage = abs(pnl) * self.slippage_buffer

        adjusted_pnl = pnl - fee - slippage

        return adjusted_pnl

    # =====================================================
    # Update
    # =====================================================

    def update(self, pnl, price=None, qty=None):

        pnl = self.apply_cost(pnl, price, qty)

        self.pnl_history.append(float(pnl))

        self.daily_pnl += pnl
        self.trade_count += 1

        if pnl < 0:
            self.loss_streak += 1
        else:
            self.loss_streak = 0

        if len(self.pnl_history) > 1000:
            self.pnl_history.pop(0)

    # =====================================================
    # CVaR
    # =====================================================

    def cvar(self):

        if len(self.pnl_history) < 20:
            return 0.0

        arr = np.array(self.pnl_history)

        var = np.percentile(arr, 5)
        tail = arr[arr <= var]

        return float(tail.mean()) if len(tail) else 0.0

    # =====================================================
    # 승률 필터
    # =====================================================

    def win_rate(self):

        if self.trade_count < 10:
            return 0.0

        wins = len([x for x in self.pnl_history if x > 0])

        return round((wins / len(self.pnl_history)) * 100, 2)

    def pass_win_rate_filter(self):

        return self.win_rate() >= self.win_rate_filter

    # =====================================================
    # Daily Loss
    # =====================================================

    def exceeded_daily_loss(self):

        return self.daily_pnl <= -abs(MAX_DAILY_LOSS)

    # =====================================================
    # Loss Streak
    # =====================================================

    def exceeded_loss_streak(self):

        return self.loss_streak >= MAX_LOSS_STREAK

    # =====================================================
    # 최종 허용 판단 (핵심)
    # =====================================================

    def allow_trade(self):

        if self.exceeded_daily_loss():
            return False

        if self.exceeded_loss_streak():
            return False

        if not self.pass_win_rate_filter():
            return False

        return True

    # =====================================================
    # Risk Score
    # =====================================================

    def risk_score(self):

        score = 100.0

        score -= min(abs(self.daily_pnl), 50)
        score -= self.loss_streak * 8

        if not self.pass_win_rate_filter():
            score -= 30

        return max(round(score, 2), 0.0)

    # =====================================================
    # Status
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


def reset_risk():
    risk_engine.__init__()
