import json
import logging
import threading
import websocket

logger = logging.getLogger(__name__)


class BybitWebSocket:

    def __init__(self):
        self.ws = None
        self.price_callback = None

    def set_price_callback(self, callback):
        self.price_callback = callback

    # =====================================================
    # MESSAGE HANDLER (FIXED)
    # =====================================================
    def on_message(self, ws, message):

        try:
            # 1. JSON 파싱
            if isinstance(message, str):
                try:
                    data = json.loads(message)
                except json.JSONDecodeError:
                    logger.warning(f"Non-JSON message ignored: {message}")
                    return
            else:
                data = message

            # 2. dict 체크
            if not isinstance(data, dict):
                return

            # 3. Bybit v5 구조 대응
            raw = data.get("data") or data.get("result")

            if raw is None:
                return

            # 4. list 구조
            if isinstance(raw, list):
                for item in raw:
                    if not isinstance(item, dict):
                        continue

                    price = item.get("lastPrice") or item.get("price")

                    if price and self.price_callback:
                        self.price_callback(float(price))

            # 5. dict 구조
            elif isinstance(raw, dict):

                price = raw.get("lastPrice") or raw.get("price")

                if price and self.price_callback:
                    self.price_callback(float(price))

        except Exception as e:
            logger.error(f"WS message error: {str(e)}")

    def on_error(self, ws, error):
        logger.error(f"WS error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logger.warning("WebSocket closed")

    def on_open(self, ws):
        logger.info("WebSocket connected")

    # =====================================================
    # START
    # =====================================================
    def start(self):

        def run():
            url = "wss://stream.bybit.com/v5/public/linear"

            self.ws = websocket.WebSocketApp(
                url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
            )

            self.ws.run_forever()

        t = threading.Thread(target=run, daemon=True)
        t.start()

        logger.info("WebSocket started")


ws_client = BybitWebSocket()
