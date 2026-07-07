import os
import requests

from config import (
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID
)


def send_message(message):
    """
    Telegram 메시지 전송
    """

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("[Telegram disabled]", message)
        return False

    try:
        url = (
            f"https://api.telegram.org/"
            f"bot{TELEGRAM_TOKEN}/sendMessage"
        )

        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }

        response = requests.post(
            url,
            data=data,
            timeout=10
        )

        return response.ok

    except Exception as e:
        print("[Telegram Error]", e)
        return False



# ==========================================
# watchdog.py 호환 객체
# ==========================================

class Telegram:

    def send(self, message):
        return send_message(message)



telegram = Telegram()
