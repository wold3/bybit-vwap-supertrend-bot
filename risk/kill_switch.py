import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class KillSwitch:

    def __init__(self):

        self.enabled = True
        self.last_reset = datetime.utcnow()

        # thresholds
        self.max_loss = -50
        self.max_drawdown_pct = -10

    # =====================================================
    # CHECK SYSTEM
    # =====================================================
    def check(self, pnl):

        if not self.enabled:
            return False

        # =========================
        # LOSS PROTECTION
        # =========================
        if pnl <= self.max_loss:
            self.trigger("MAX LOSS HIT")
            return False

        return True

    # =====================================================
    # TRIGGER STOP
    # =====================================================
    def trigger(self, reason):

        self.enabled = False
        logger.error(f"KILL SWITCH ACTIVATED: {reason}")

    # =====================================================
    # RESET
    # =====================================================
    def reset(self):

        self.enabled = True
        self.last_reset = datetime.utcnow()

        logger.info("KILL SWITCH RESET")


kill_switch = KillSwitch()
