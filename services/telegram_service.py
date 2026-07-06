import requests
import logging
from datetime import datetime

from risk.risk_engine import risk_engine

logger = logging.getLogger(__name__)


class TelegramService:

    def __init__(self, token, chat_id):

        self.token = token
        self.chat_id = chat_id

        self.url = f"https://api.telegram.org/bot{token}/sendMessage"

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
            requests.post(self.url, data=payload, timeout=5)
        except Exception as e:
            logger.error(f"Telegram error: {str(e)}")

    # =====================================================
    # 거래 알림
    # =====================================================

    def trade(self, symbol, side, qty, price, pnl=None):

        msg = f"""
📊 <b>TRADE</b>
────────────────
Symbol: {symbol}
Side: {side}
Qty: {qty}
Price: {price}
"""

        if pnl is not None:
            msg += f"PnL: {round(pnl, 4)}\n"

        msg += f"Time: {datetime.utcnow()}\n"

        self.send(msg)

    # =====================================================
    # 리스크 상태 알림 (업그레이드)
    # =====================================================

    def risk_update(self):

        s = risk_engine.status()

        emoji = "🟢"

        if s["risk_score"] < 40:
            emoji = "🔴"
        elif s["risk_score"] < 70:
            emoji = "🟡"

        msg = f"""
{emoji} <b>RISK STATUS</b>
────────────────
PnL: {s['daily_pnl']}
Win Rate: {s['win_rate']}%
Loss Streak: {s['loss_streak']}
Drawdown: {s['drawdown']}
Risk Score: {s['risk_score']}
Mode: {s['regime_bias']}
Allow Trade: {s['allow_trade']}
Time: {datetime.utcnow()}
"""

        self.send(msg)

    # =====================================================
    # 드로우다운 경고 (핵심 추가)
    # =====================================================

    def drawdown_alert(self):

        s = risk_engine.status()

        if s["drawdown"] > 0.1:

            msg = f"""
🚨 <b>DRAWDOWN ALERT</b>
────────────────
Drawdown: {s['drawdown']}
Risk Mode: {s['regime_bias']}
Action: REDUCE RISK
Time: {datetime.utcnow()}
"""

            self.send(msg)

    # =====================================================
    # 수익 폭발 알림
    # =====================================================

    def profit_spike(self):

        s = risk_engine.status()

        if s["daily_pnl"] > 50:

            msg = f"""
🚀 <b>PROFIT SPIKE</b>
────────────────
PnL: {s['daily_pnl']}
Mode: {s['regime_bias']}
Action: SCALE UP POSSIBLE
Time: {datetime.utcnow()}
"""

            self.send(msg)

    # =====================================================
    # 에러 알림
    # =====================================================

    def error(self, error):

        msg = f"""
🚨 <b>ERROR</b>
────────────────
{str(error)}
Time: {datetime.utcnow()}
"""

        self.send(msg)

    # =====================================================
    # heartbeat
    # =====================================================

    def heartbeat(self):

        s = risk_engine.status()

        msg = f"""
💓 <b>HEARTBEAT</b>
────────────────
PnL: {s['daily_pnl']}
Trades: {s['trade_count']}
Risk: {s['risk_score']}
Drawdown: {s['drawdown']}
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
