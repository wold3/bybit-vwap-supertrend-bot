import logging
from datetime import datetime

from risk.risk_engine import risk_engine

logger = logging.getLogger(__name__)


class KillSwitch:

    def __init__(self):

        self.enabled = True
        self.disabled_reason = None
        self.disabled_time = None

    # =====================================================
    # Check Status
    # =====================================================
    def check(self):

        status = risk_engine.status()

        # 1. 일일 손실 제한
        if status["daily_limit"]:
            self.disable("daily_loss_limit")
            return False

        # 2. 연속 손실 제한
        if status["loss_limit"]:
            self.disable("loss_streak_limit")
            return False

        # 3. 위험 점수 체크
        if status["risk_score"] < 30:
            self.disable("low_risk_score")
            return False

        return True

    # =====================================================
    # Disable Trading
    # =====================================================
    def disable(self, reason: str):

        if not self.enabled:
            return

        self.enabled = False
        self.disabled_reason = reason
        self.disabled_time = datetime.utcnow()

        logger.warning("KILL SWITCH ACTIVATED: %s", reason)

    # =====================================================
    # Enable Trading
    # =====================================================
    def enable(self):

        self.enabled = True
        self.disabled_reason = None
        self.disabled_time = None

        logger.info("KILL SWITCH RESET")

    # =====================================================
    # Status
    # =====================================================
    def status(self):

        return {
            "enabled": self.enabled,
            "reason": self.disabled_reason,
            "disabled_time": (
                self.disabled_time.isoformat()
                if self.disabled_time
                else None
            ),
        }


# =====================================================
# Singleton
# =====================================================
kill_switch = KillSwitch()


# =====================================================
# Global Check Function
# =====================================================
def allow_trading():

    return kill_switch.enabled and kill_switch.check()
