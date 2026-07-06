import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class TelegramService:

    def __init__(self, token, chat_id):

        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"

    # =====================================================
    # Send Message
    # =====================================================
    def send_message(self, text):

        try:

            url = f"{self.base_url}/sendMessage"

            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "HTML"
            }

            requests.post(url, data=payload, timeout=5)

        except Exception as e:
            logger.error("Telegram send failed: %s", e)

    # =====================================================
    # Trade Alert
    # =====================================================
    def send_trade(self, signal, symbol, qty, price):

        msg = f"""
📊 <b>TRADE EXECUTED</b>

📌 Signal: {signal}
💱 Symbol: {symbol}
📦 Qty: {qty}
💰 Price: {price}
🕒 Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
"""

        self.send_message(msg)

    # =====================================================
    # Error Alert
    # =====================================================
    def send_error(self, error):

        msg = f"""
🚨 <b>ERROR ALERT</b>

{error}

🕒 {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}
"""

        self.send_message(msg)

    # =====================================================
    # Daily Report
    # =====================================================
    def send_daily_report(self, pnl, trades, win_rate):

        msg = f"""
📈 <b>DAILY REPORT</b>

💰 PnL: {pnl}
📊 Trades: {trades}
🎯 Win Rate: {win_rate}%

🕒 {datetime.utcnow().strftime('%Y-%m-%d')}
"""

        self.send_message(msg)


# =====================================================
# Singleton
# =====================================================
telegram_service = TelegramService(
    token="YOUR_BOT_TOKEN",
    chat_id="YOUR_CHAT_ID"
)
