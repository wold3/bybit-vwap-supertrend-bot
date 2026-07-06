import json
import logging
import websocket
import threading

logger = logging.getLogger(__name__)


class BybitWebSocket:

    def __init__(self):
        self.ws = None
        self.callback = None
        self.running = False

    # =====================================================
    def set_price_callback(self, cb):
        self.callback = cb

    # =====================================================
    def safe_parse(self, msg):
        if isinstance(msg, str):
            try:
                return json.loads(msg)
            except:
                return None
        return msg

    # =====================================================
    def on_message(self, ws, message):

        try:
            data = self.safe_parse(message)

            if not isinstance(data, dict):
                return

            # BYBIT 구조 대응
            if "data" in data:
                inner = data["data"]

                if isinstance(inner, list) and len(inner) > 0:
                    item = inner[0]

                    if isinstance(item, dict):
                        price = item.get("lastPrice") or item.get("price")

                        if price and self.callback:
                            self.callback(float(price))

        except Exception as e:
            logger.error(f"WS message error: {e}")

    # =====================================================
    def on_open(self, ws):
        logger.info("WebSocket connected")

    def on_close(self, ws, *args):
        logger.warning("WebSocket closed")

    def on_error(self, ws, error):
        logger.error(f"WebSocket error: {error}")

    # =====================================================
    def start(self):

        self.running = True

        logger.info("WebSocket started")

        url = "wss://stream.bybit.com/v5/public/linear"

        self.ws = websocket.WebSocketApp(
            url,
            on_message=self.on_message,
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error
        )

        t = threading.Thread(
            target=self.ws.run_forever,
            daemon=True
        )
        t.start()

    # =====================================================
    def stop(self):
        self.running = False
        if self.ws:
            self.ws.close()
        logger.info("WebSocket stopped")


ws_client = BybitWebSocket()
