import logging
import requests

from config import (
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
)

logger = logging.getLogger(__name__)

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


def send(text, parse_mode=None):
    """
    Telegram 메시지 전송

    Args:
        text (str): 전송할 메시지
        parse_mode (str|None): "Markdown" 또는 "HTML"

    Returns:
        bool
    """

    if not TELEGRAM_TOKEN:
        logger.debug("Telegram token is not configured.")
        return False

    if not TELEGRAM_CHAT_ID:
        logger.debug("Telegram chat id is not configured.")
        return False

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": str(text),
    }

    if parse_mode:
        payload["parse_mode"] = parse_mode

    try:

        response = requests.post(
            f"{BASE_URL}/sendMessage",
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        result = response.json()

        if not result.get("ok", False):
            logger.error(
                "Telegram API Error: %s",
                result
            )
            return False

        logger.info("Telegram message sent.")

        return True

    except requests.exceptions.RequestException as e:

        logger.exception("Telegram request failed: %s", e)

        return False


def send_trade(action, symbol, qty, price=None):
    """
    거래 알림 전송
    """

    message = (
        "📈 Bybit AI Bot\n\n"
        f"Action : {action}\n"
        f"Symbol : {symbol}\n"
        f"Qty    : {qty}"
    )

    if price:
        message += f"\nPrice  : {price}"

    return send(message)


def send_error(error):
    """
    오류 알림
    """

    return send(
        f"❌ Bot Error\n\n{error}"
    )


def send_status(status):
    """
    상태 알림
    """

    return send(
        f"ℹ️ {status}"
    )
