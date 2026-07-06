import json
import logging
import websocket
import threading

from services.event_bus import event_bus

logger = logging.getLogger(__name__)


class BybitWebSocket:

    def __init__(self):
        self.ws = None

    def start(self):

        def run():

            self.ws = websocket.WebSocketApp(
                "wss://stream.bybit.com/v5/public/linear",
                on_message=self.on_message,
                on_open=self.on_open,
                on_close=self.on_close,
                on_error=self.on_error
            )

            logger.info("WebSocket started")
            self.ws.run_forever()

        threading.Thread(target=run, daemon=True).start()

    def on_message(self, ws, message):

        try:

            if isinstance(message, bytes):
                message = message.decode("utf-8")

            data = json.loads(message)

            if "topic" in data and "tickers" in data.get("topic", ""):

                items = data.get("data", [])

                if isinstance(items, list):

                    for item in items:

                        if not isinstance(item, dict):
                            continue

                        price = item.get("lastPrice")

                        if price is None:
                            continue

                        event_bus.publish({
                            "type": "PRICE",
                            "symbol": item.get("symbol"),
                            "price": float(price)
                        })

        except Exception as e:
            logger.error(f"WS error: {str(e)}")

    def on_open(self, ws):
        logger.info("WebSocket connected")

    def on_close(self, ws, *args):
        logger.warning("WebSocket closed")

    def on_error(self, ws, error):
        logger.error(f"WS error: {error}")


ws_client = BybitWebSocket()
