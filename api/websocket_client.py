import json
import logging
import threading
import websocket
import time

logger = logging.getLogger(__name__)


class BybitWebSocket:

    def __init__(self):
        self.ws = None
        self.price_callback = None
        self.running = False

    def set_price_callback(self, callback):
        self.price_callback = callback

    # =====================================================
    # MESSAGE HANDLER
    # =====================================================
    def on_message(self, ws, message):

        try:
            if message in ("ping", "pong"):
                return

            if isinstance(message, str):
                try:
                    data = json.loads(message)
                except:
                    return
            else:
                data = message

            if not isinstance(data, dict):
                return

            raw = data.get("data") or data.get("result")

            if not raw:
                return

            if isinstance(raw, list):
                for item in raw:
                    if not isinstance(item, dict):
                        continue

                    price = item.get("lastPrice") or item.get("price")

                    if price and self.price_callback:
                        self.price_callback(float(price))

            elif isinstance(raw, dict):

                price = raw.get("lastPrice") or raw.get("price")

                if price and self.price_callback:
                    self.price_callback(float(price))

        except Exception as e:
            logger.error(f"WS error: {e}")

    def on_error(self, ws, error):
        logger.error(f"WS error: {error}")

    def on_close(self, ws, *args):
        logger.warning("WebSocket closed")
        self.running = False

        time.sleep(3)
        if self.running:
            self.start()

    def on_open(self, ws):
        logger.info("WebSocket connected")

    # =====================================================
    # START
    # =====================================================
    def start(self):

        self.running = True

        def run():
            url = "wss://stream.bybit.com/v5/public/linear"

            while self.running:
                try:
                    self.ws = websocket.WebSocketApp(
                        url,
                        on_open=self.on_open,
                        on_message=self.on_message,
                        on_error=self.on_error,
                        on_close=self.on_close,
                    )

                    self.ws.run_forever(ping_interval=20, ping_timeout=10)

                except Exception as e:
                    logger.error(f"WS loop error: {e}")
                    time.sleep(3)

        threading.Thread(target=run, daemon=True).start()

        logger.info("WebSocket started")


ws_client = BybitWebSocket()
