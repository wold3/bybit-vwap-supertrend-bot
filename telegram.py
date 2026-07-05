import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def send_message(text):

    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }

    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("[TELEGRAM ERROR]", e)
