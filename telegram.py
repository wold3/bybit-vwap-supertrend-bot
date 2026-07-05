import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def send_message(text):

    if not TELEGRAM_TOKEN:
        return

    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text},
            timeout=5
        )
    except:
        pass
