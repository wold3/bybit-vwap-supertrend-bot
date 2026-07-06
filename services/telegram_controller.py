import logging

from execution.execution_engine import engine
from risk.risk_engine import risk_engine, reset_risk
from database.repository import get_summary, get_recent_trades

logger = logging.getLogger(__name__)


class TelegramController:

    def __init__(self):

        self.commands = {
            "/status": self.status,
            "/summary": self.summary,
            "/risk": self.risk,
            "/reset_risk": self.reset_risk,
            "/trades": self.trades,
            "/engine": self.engine_status,
        }

    # =====================================================
    # Router
    # =====================================================
    def handle(self, text: str):

        cmd = text.split(" ")[0]

        handler = self.commands.get(cmd)

        if not handler:
            return "Unknown command"

        return handler()

    # =====================================================
    # Status
    # =====================================================
    def status(self):

        return {
            "engine": engine.status(),
            "risk": risk_engine.status(),
        }

    # =====================================================
    # Summary
    # =====================================================
    def summary(self):

        return get_summary()

    # =====================================================
    # Risk
    # =====================================================
    def risk(self):

        return risk_engine.status()

    # =====================================================
    # Reset Risk
    # =====================================================
    def reset_risk(self):

        reset_risk()

        return {
            "result": "risk reset done"
        }

    # =====================================================
    # Trades
    # =====================================================
    def trades(self):

        return get_recent_trades(20)

    # =====================================================
    # Engine Status
    # =====================================================
    def engine_status(self):

        return engine.status()


# =====================================================
# Singleton
# =====================================================
telegram_controller = TelegramController()
