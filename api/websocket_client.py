import json
import websocket
import threading
import logging

from services.event_bus import event_bus

logger = logging.getLogger(__name__)


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

        try:

            data = json.loads(message)

            topic = data.get("topic", "")

            # ORDERBOOK
            if "orderbook" in topic:

                event_bus.publish({
                    "type": "ORDERBOOK",
                    "symbol": data.get("symbol"),
                    "bids": data.get("data", {}).get("b", []),
                    "asks": data.get("data", {}).get("a", [])
                })

            # TICKER
            if "tickers" in topic:

                for item in data.get("data", []):

                    event_bus.publish({
                        "type": "TICK",
                        "symbol": item.get("symbol"),
                        "price": float(item.get("lastPrice", 0))
                    })

        except Exception as e:
            logger.error(f"WS ERROR: {e}")


ws_client = BybitWebSocket()
