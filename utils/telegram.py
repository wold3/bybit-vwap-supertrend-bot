import requests

class Telegram:

    def __init__(self):
        self.token = "YOUR_TOKEN"
        self.chat_id = "YOUR_CHAT_ID"

    def send(self, msg):

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        try:
            requests.post(url, data={
                "chat_id": self.chat_id,
                "text": msg
            })
        except:
            pass

telegram = Telegram()
