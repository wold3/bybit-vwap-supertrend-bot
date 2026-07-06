import logging
import requests

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)


class TelegramService:

    def __init__(self):

        self.base_url = (
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
        )

    # =====================================================
    # Send Message
    # =====================================================
    def send_message(self, text: str):

        try:

            url = f"{self.base_url}/sendMessage"

            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "HTML",
            }

            response = requests.post(url, json=payload, timeout=5)

            if not response.ok:

                logger.error(
                    "Telegram send failed: %s",
                    response.text,
                )

                return False

            return True

        except Exception as e:

            logger.exception(e)

            return False

    # =====================================================
    # Trade Alert
    # =====================================================
    def send_trade(self, signal, symbol, qty, price):

        message = (
            f"🚀 <b>TRADE EXECUTED</b>\n"
            f"Signal: {signal}\n"
            f"Symbol: {symbol}\n"
            f"Qty: {qty}\n"
            f"Price: {price}"
        )

        return self.send_message(message)

    # =====================================================
    # Error Alert
    # =====================================================
    def send_error(self, error: str):

        message = (
            f"❌ <b>ERROR</b>\n"
            f"{error}"
        )

        return self.send_message(message)

    # =====================================================
    # Risk Alert
    # =====================================================
    def send_risk(self, reason: str):

        message = (
            f"⚠️ <b>RISK BLOCKED</b>\n"
            f"Reason: {reason}"
        )

        return self.send_message(message)

    # =====================================================
    # Position Alert
    # =====================================================
    def send_position(self, symbol, pnl):

        message = (
            f"📊 <b>POSITION UPDATE</b>\n"
            f"Symbol: {symbol}\n"
            f"PnL: {pnl}"
        )

        return self.send_message(message)


# =====================================================
# Singleton
# =====================================================
telegram_service = TelegramService()


# =====================================================
# Compatibility Wrappers (기존 코드 호환)
# =====================================================
def send_trade(signal, symbol, qty, price):
    return telegram_service.send_trade(signal, symbol, qty, price)


def send_error(error: str):
    return telegram_service.send_error(error)


def send_risk(reason: str):
    return telegram_service.send_risk(reason)


def send_position(symbol, pnl):
    return telegram_service.send_position(symbol, pnl)
