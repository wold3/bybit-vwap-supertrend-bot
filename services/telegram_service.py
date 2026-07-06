import logging
import requests
from datetime import datetime

from risk.risk_engine import risk_engine

logger = logging.getLogger(__name__)


class TelegramService:

    def __init__(self, token, chat_id):

        self.token = token
        self.chat_id = chat_id

        self.base_url = f"https://api.telegram.org/bot{token}/sendMessage"

    # =====================================================
    # 기본 전송
    # =====================================================

    def send(self, message):

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        try:
            requests.post(self.base_url, data=payload, timeout=5)
        except Exception as e:
            logger.error(f"Telegram send error: {str(e)}")

    # =====================================================
    # 거래 알림
    # =====================================================

    def notify_trade(self, symbol, side, qty, price, pnl=None):

        msg = f"""
📊 <b>TRADE EXECUTED</b>
────────────────
Symbol: {symbol}
Side: {side}
Qty: {qty}
Price: {price}
"""

        if pnl is not None:
            msg += f"PnL: {pnl}\n"

        msg += f"Time: {datetime.utcnow()}\n"

        self.send(msg)

    # =====================================================
    # 리스크 알림
    # =====================================================

    def notify_risk(self):

        status = risk_engine.status()

        msg = f"""
⚠️ <b>RISK UPDATE</b>
────────────────
Daily PnL: {status['daily_pnl']}
Win Rate: {status['win_rate']}%
Risk Score: {status['risk_score']}
Loss Streak: {status['loss_streak']}
Allow Trade: {status['allow_trade']}
"""

        self.send(msg)

    # =====================================================
    # 에러 알림
    # =====================================================

    def notify_error(self, error):

        msg = f"""
🚨 <b>ERROR</b>
────────────────
{str(error)}
Time: {datetime.utcnow()}
"""

        self.send(msg)

    # =====================================================
    # 상태 체크
    # =====================================================

    def heartbeat(self):

        status = risk_engine.status()

        msg = f"""
💓 <b>HEARTBEAT</b>
────────────────
PnL: {status['daily_pnl']}
Trades: {status['trade_count']}
Risk: {status['risk_score']}
Time: {datetime.utcnow()}
"""

        self.send(msg)


# =====================================================
# Singleton
# =====================================================

telegram_service = None


def init_telegram(token, chat_id):
    global telegram_service
    telegram_service = TelegramService(token, chat_id)
    return telegram_service


def get_telegram():
    return telegram_service
