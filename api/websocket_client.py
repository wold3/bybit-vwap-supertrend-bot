import json
import websocket
import threading
import time
from services.event_bus import event_bus
import logging

logger = logging.getLogger(__name__)


class WSClient:

    def __init__(self):
        self.ws = None

    # =====================================================
    # START LOOP
    # =====================================================
    def start(self):

        t = threading.Thread(target=self.run, daemon=True)
        t.start()

    # =====================================================
    # AUTO RECONNECT
    # =====================================================
    def run(self):

        while True:

            try:

                self.ws = websocket.WebSocketApp(
                    "wss://stream.bybit.com/v5/public/linear",
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close
                )

                self.ws.run_forever(ping_interval=20)

            except Exception as e:
                logger.error(f"WS CRASH: {e}")

            print("WS reconnect in 3 sec...")
            time.sleep(3)

    # =====================================================
    # MESSAGE
    # =====================================================
    def on_message(self, ws, msg):

        try:

            data = json.loads(msg)

            if "topic" in data and "tickers" in data["topic"]:

                for item in data.get("data", []):

                    event_bus.put({
                        "type": "TICK",
                        "symbol": item.get("symbol"),
                        "price": float(item.get("lastPrice", 0))
                    })

        except Exception as e:
            logger.error(f"WS ERROR: {e}")

    def on_error(self, ws, err):
        logger.error(f"WS ERROR: {err}")

    def on_close(self, ws, code, msg):
        logger.warning(f"WS CLOSED: {code} {msg}")


ws_client = WSClient()
