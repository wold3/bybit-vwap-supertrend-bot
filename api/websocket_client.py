import json
import logging
import websocket
import threading
import time

from services.event_bus import event_bus

logger = logging.getLogger(__name__)


class BybitWebSocket:

    def __init__(self):
        self.ws = None
        self.running = True

    # =====================================================
    # START (AUTO RECONNECT)
    # =====================================================
    def start(self):

        def run():

            while self.running:

                try:

                    self.ws = websocket.WebSocketApp(
                        "wss://stream.bybit.com/v5/public/linear",
                        on_message=self.on_message,
                        on_open=self.on_open,
                        on_close=self.on_close,
                        on_error=self.on_error
                    )

                    self.ws.run_forever()

                except Exception as e:
                    logger.error(f"WS CRASH: {e}")

                logger.warning("WS reconnect in 3s...")
                time.sleep(3)

        threading.Thread(target=run, daemon=True).start()

    # =====================================================
    # MESSAGE
    # =====================================================
    def on_message(self, ws, message):

        try:

            if isinstance(message, bytes):
                message = message.decode()

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
            logger.error(f"WS ERROR: {e}")

    def on_open(self, ws):
        logger.info("WS CONNECTED")

    def on_close(self, ws, *args):
        logger.warning("WS CLOSED")

    def on_error(self, ws, error):
        logger.error(f"WS ERROR: {error}")


ws_client = BybitWebSocket()
