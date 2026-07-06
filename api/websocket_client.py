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

    # =====================================================
    # ON MESSAGE (FIX 핵심)
    # =====================================================
    def on_message(self, ws, message):

        try:
            # 1) string → dict 변환
            if isinstance(message, str):
                data = json.loads(message)
            else:
                data = message

            # 2) Bybit v5 대응
            if not isinstance(data, dict):
                return

            # Bybit WS 구조: data / result / topic 혼재
            payload = None

            if "data" in data:
                payload = data["data"]
            elif "result" in data:
                payload = data["result"]
            elif "price" in data:
                payload = data

            if payload is None:
                return

            # list 구조
            if isinstance(payload, list):
                for item in payload:
                    self._handle_item(item)

            # dict 구조
            elif isinstance(payload, dict):
                self._handle_item(payload)

        except json.JSONDecodeError:
            logger.error(f"WS JSON decode failed: {message}")

        except Exception as e:
            logger.error(f"WS message error: {str(e)}")

    # =====================================================
    # ITEM HANDLER
    # =====================================================
    def _handle_item(self, item):

        try:
            if not isinstance(item, dict):
                return

            price = None
            volume = None

            if "lastPrice" in item:
                price = float(item.get("lastPrice", 0))
                volume = float(item.get("volume24h", 0))

            elif "price" in item:
                price = float(item.get("price", 0))

            if price is not None and self.price_callback:
                self.price_callback(price, volume or 0)

        except Exception as e:
            logger.error(f"Item parse error: {e}")

    # =====================================================
    # START
    # =====================================================
    def start(self):

        def run():
            self.ws = websocket.WebSocketApp(
                "wss://stream.bybit.com/v5/public/linear",
                on_message=self.on_message,
                on_open=lambda ws: logger.info("WebSocket connected"),
                on_error=lambda ws, e: logger.error(f"WS error: {e}"),
                on_close=lambda ws, c, m: logger.warning("WebSocket closed")
            )
            self.ws.run_forever()

        t = threading.Thread(target=run)
        t.daemon = True
        t.start()

        logger.info("WebSocket started")


ws_client = BybitWebSocket()
