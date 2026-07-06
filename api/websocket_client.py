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

        try:

            # =========================
            # SAFE PARSE (핵심 수정)
            # =========================
            if isinstance(msg, str):
                data = json.loads(msg)
            else:
                data = msg

            if not isinstance(data, dict):
                return

            topic = data.get("topic", "")

            if "tickers" in topic:

                for item in data.get("data", []):

                    # 추가 안전장치
                    if not isinstance(item, dict):
                        continue

                    event_bus.put({
                        "type": "TICK",
                        "symbol": item.get("symbol"),
                        "price": float(item.get("lastPrice", 0))
                    })

        except Exception as e:
            print(f"WS message error: {e}")


ws_client = WS()
