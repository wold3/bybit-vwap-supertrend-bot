import json
import websocket
import threading
from services.event_bus import event_bus


class WS:

    def start(self):

        def run():

            ws = websocket.WebSocketApp(
                "wss://stream.bybit.com/v5/public/linear",
                on_message=self.on_message
            )

            ws.run_forever()

        threading.Thread(target=run, daemon=True).start()

    def on_message(self, ws, msg):

        data = json.loads(msg)

        if "topic" in data and "tickers" in data["topic"]:

            for i in data.get("data", []):

                event_bus.put({
                    "type": "TICK",
                    "symbol": i["symbol"],
                    "price": float(i["lastPrice"])
                })


ws_client = WS()
