import logging
from datetime import datetime

from database.repository import (
    get_summary,
    get_today_pnl,
)

from risk.risk_engine import get_risk_status

from execution.position_manager import position_manager

from telegram_service import send_trade

logger = logging.getLogger(__name__)


class ReportService:

    def __init__(self):
        pass

    # =====================================================
    # Daily Report
    # =====================================================
    def send_daily_report(self):

        try:

            today = datetime.utcnow().strftime("%Y-%m-%d")

            summary = get_summary()
            risk = get_risk_status()
            position = position_manager.status()
            pnl_today = get_today_pnl(today)

            message = (
                "📊 <b>DAILY REPORT</b>\n\n"
                f"💰 PnL Today: {pnl_today}\n"
                f"📈 Total Trades: {summary.get('trade_count')}\n"
                f"🏆 Wins: {summary.get('wins')}\n"
                f"❌ Losses: {summary.get('losses')}\n"
                f"🎯 Win Rate: {summary.get('win_rate', 0)}%\n\n"
                f"⚠️ Risk Score: {risk.get('risk_score')}\n"
                f"🔥 Loss Streak: {risk.get('loss_streak')}\n\n"
                f"📦 Position Active: {position.get('active')}\n"
            )

            send_trade("REPORT", "SYSTEM", 0, message)

            logger.info("Daily report sent")

        except Exception as e:

            logger.exception(e)

    # =====================================================
    # Status Report
    # =====================================================
    def send_status_report(self):

        try:

            summary = get_summary()
            risk = get_risk_status()

            message = (
                "📡 <b>SYSTEM STATUS</b>\n\n"
                f"Trades: {summary.get('trade_count')}\n"
                f"PnL: {summary.get('total_pnl')}\n"
                f"Risk Score: {risk.get('risk_score')}\n"
                f"Allow Trade: {risk.get('allow_trade')}\n"
            )

            send_trade("STATUS", "SYSTEM", 0, message)

        except Exception as e:

            logger.exception(e)


# =====================================================
# Singleton
# =====================================================
report_service = ReportService()


# =====================================================
# Helper Functions
# =====================================================
def send_daily_report():
    return report_service.send_daily_report()


def send_status_report():
    return report_service.send_status_report()
