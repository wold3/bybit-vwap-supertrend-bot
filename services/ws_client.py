import json
import websocket

from dashboard.app import update_price, update_equity


class BybitWSClient:

    def __init__(self, url):
        self.url = url

    def on_message(self, ws, message):

        data = json.loads(message)

        try:
            if "data" in data:

                trades = data["data"]

                if trades:

                    price = float(trades[-1]["p"])

                    # ============================
                    # PRICE UPDATE
                    # ============================
                    update_price(price)

                    # ============================
                    # MOCK EQUITY UPDATE
                    # ============================
                    pnl = price % 1000  # (예시 - 실제는 position pnl)

                    update_equity(pnl)

        except Exception as e:
            print("[WS ERROR]", e)

    def on_open(self, ws):
        print("WS CONNECTED")

    def start(self):

        ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_open=self.on_open
        )

        ws.run_forever()


def start_ws():

    url = "wss://stream.bybit.com/v5/public/linear"

    client = BybitWSClient(url)
    client.start()
