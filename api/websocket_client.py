import json
import logging
import websocket
import threading

logger = logging.getLogger(__name__)


class BybitWebSocket:

    def __init__(self):
        self.ws = None
        self.price_callback = None

    def set_price_callback(self, callback):
        self.price_callback = callback

    # =========================
    # MESSAGE HANDLER
    # =========================
    def on_message(self, ws, message):

        try:
            # ✅ 1. 문자열이면 JSON 변환
            if isinstance(message, str):
                try:
                    data = json.loads(message)
                except Exception:
                    logger.error(f"WS raw message (not json): {message}")
                    return
            else:
                data = message

            # =========================
            # Bybit 구조 대응
            # =========================
            if isinstance(data, dict):

                # Bybit v5 ticker format 대응
                result = data.get("data") or data.get("result")

                if isinstance(result, list) and len(result) > 0:
                    item = result[0]

                    price = item.get("lastPrice") or item.get("price")

                    if price and self.price_callback:
                        self.price_callback(float(price))

                elif isinstance(result, dict):
                    price = result.get("lastPrice") or result.get("price")

                    if price and self.price_callback:
                        self.price_callback(float(price))

            else:
                logger.error(f"WS unknown format: {type(data)}")

        except Exception as e:
            logger.error(f"WS message error: {str(e)}")

    def on_error(self, ws, error):
        logger.error(f"WS error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logger.warning("WebSocket closed")

    def on_open(self, ws):
        logger.info("WebSocket connected")

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
