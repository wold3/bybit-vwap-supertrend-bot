import json
import websocket
import threading

from services.event_bus import event_bus


class BybitWebSocket:

    def start(self):

        def run():

            ws = websocket.WebSocketApp(
                "wss://stream.bybit.com/v5/public/linear",
                on_message=self.on_message
            )

            ws.run_forever()

        threading.Thread(target=run, daemon=True).start()

    def on_message(self, ws, message):

        data = json.loads(message)

        if "topic" in data and "tickers" in data["topic"]:

            for item in data.get("data", []):

                event_bus.publish({
                    "type": "TICK",
                    "symbol": item["symbol"],
                    "price": float(item["lastPrice"])
                })


ws_client = BybitWebSocket()
