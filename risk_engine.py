import logging
from datetime import datetime

import numpy as np

from config import (
    MAX_DAILY_LOSS,
    MAX_LOSS_STREAK,
)

logger = logging.getLogger(__name__)


class RiskEngine:

    def __init__(self):

        self.pnl_history = []

        self.daily_pnl = 0.0

        self.loss_streak = 0

        self.trade_count = 0

        self.max_position = 1

        self.last_reset = datetime.utcnow().date()

    # =====================================================
    # Daily Reset
    # =====================================================

    def _check_reset(self):

        today = datetime.utcnow().date()

        if today != self.last_reset:

            logger.info("Daily Risk Reset")

            self.daily_pnl = 0.0

            self.trade_count = 0

            self.loss_streak = 0

            self.last_reset = today

    # =====================================================
    # Update PnL
    # =====================================================

    def update(self, pnl):

        self._check_reset()

        pnl = float(pnl)

        self.pnl_history.append(pnl)

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

        if len(tail) == 0:

            return 0.0

        return float(tail.mean())
    
    # =====================================================
    # Daily Loss Limit
    # =====================================================

    def exceeded_daily_loss(self):

        return self.daily_pnl <= -abs(MAX_DAILY_LOSS)

    # =====================================================
    # Loss Streak
    # =====================================================

    def exceeded_loss_streak(self):

        return self.loss_streak >= MAX_LOSS_STREAK

    # =====================================================
    # Trade Permission
    # =====================================================

    def allow_trade(self):

        self._check_reset()

        if self.exceeded_daily_loss():

            logger.warning(
                "Daily loss limit exceeded."
            )

            return False

        if self.exceeded_loss_streak():

            logger.warning(
                "Loss streak exceeded."
            )

            return False

        return True

    # =====================================================
    # Risk Score
    # =====================================================

    def risk_score(self):

        score = 100.0

        score -= min(
            abs(self.daily_pnl),
            100,
        )

        score -= self.loss_streak * 10

        score -= min(
            self.trade_count,
            20,
        )

        return max(
            round(score, 2),
            0.0,
        )

    # =====================================================
    # Status
    # =====================================================

    def status(self):

        self._check_reset()

        return {

            "daily_pnl": round(
                self.daily_pnl,
                2,
            ),

            "trade_count": self.trade_count,

            "loss_streak": self.loss_streak,

            "risk_score": self.risk_score(),

            "daily_limit": self.exceeded_daily_loss(),

            "loss_limit": self.exceeded_loss_streak(),

            "allow_trade": self.allow_trade(),

            "cvar": round(
                self.cvar(),
                4,
            ),
        }

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        logger.info(
            "Risk Engine Reset"
        )

        self.pnl_history.clear()

        self.daily_pnl = 0.0

        self.trade_count = 0

        self.loss_streak = 0

        self.last_reset = datetime.utcnow().date()

    # =====================================================
    # Health
    # =====================================================

    def health(self):

        self._check_reset()

        return {

            "engine": "RiskEngine",

            "healthy": True,

            "daily_pnl": round(
                self.daily_pnl,
                2,
            ),

            "trade_count": self.trade_count,

            "loss_streak": self.loss_streak,

            "risk_score": self.risk_score(),

            "allow_trade": self.allow_trade(),
        }

    # =====================================================
    # Export
    # =====================================================

    def export(self):

        return {

            "daily_pnl": self.daily_pnl,

            "trade_count": self.trade_count,

            "loss_streak": self.loss_streak,

            "cvar": self.cvar(),

            "risk_score": self.risk_score(),

            "allow_trade": self.allow_trade(),

            "last_reset": str(self.last_reset),
        }

    # =====================================================
    # __repr__
    # =====================================================

    def __repr__(self):

        return (
            f"<RiskEngine "
            f"daily_pnl={self.daily_pnl} "
            f"loss_streak={self.loss_streak} "
            f"risk_score={self.risk_score()}>"
        )


# =====================================================
# Singleton
# =====================================================

risk_engine = RiskEngine()


# =====================================================
# Compatibility Wrapper
# =====================================================

def allow_trade():

    """
    execution_engine.py와의 기존 호환성을 유지하기 위한 Wrapper
    """

    return risk_engine.allow_trade()


def update_risk(pnl):

    """
    거래 종료 후 손익 업데이트
    """

    risk_engine.update(pnl)


def get_risk_status():

    return risk_engine.status()


def reset_risk():

    risk_engine.reset()


# =====================================================
# Module Export
# =====================================================

__all__ = [
    "RiskEngine",
    "risk_engine",
    "allow_trade",
    "update_risk",
    "get_risk_status",
    "reset_risk",
]
        
