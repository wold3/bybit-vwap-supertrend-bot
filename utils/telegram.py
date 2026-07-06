import requests


class TelegramBot:

    def __init__(self, token, chat_id):

        self.token = token
        self.chat_id = chat_id

    # ================================
    # SEND MESSAGE
    # ================================
    def send(self, message):

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        try:
            requests.post(url, data={
                "chat_id": self.chat_id,
                "text": message
            })
        except Exception as e:
            print(f"Telegram error: {e}")


# ================================
# CONFIG (여기만 수정하면 됨)
# ================================
telegram = TelegramBot(
    token="YOUR_BOT_TOKEN",
    chat_id="YOUR_CHAT_ID"
)
