import json
import websocket
import threading
import time
from services.event_bus import event_bus

class WSClient:

    def start(self):

        t = threading.Thread(target=self.run, daemon=True)
        t.start()

    def run(self):

        while True:

            ws = websocket.WebSocketApp(
                "wss://stream.bybit.com/v5/public/linear",
                on_message=self.on_message
            )

            ws.run_forever(ping_interval=20)

            time.sleep(3)

    def on_message(self, ws, msg):

        try:
            data = json.loads(msg)
        except:
            return

        if "tickers" not in data.get("topic", ""):
            return

        for i in data.get("data", []):

            event_bus.put({
                "type": "TICK",
                "symbol": i.get("symbol"),
                "price": float(i.get("lastPrice", 0))
            })

ws_client = WSClient()
