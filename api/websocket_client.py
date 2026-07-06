import json
import logging
import websocket
import threading

logger = logging.getLogger(__name__)


class BybitWebSocket:

    def __init__(self):
        self.ws = None
        self.url = "wss://stream.bybit.com/v5/public/linear"
        self.callback = None

    # =====================================================
    # CALLBACK
    # =====================================================
    def set_price_callback(self, callback):
        self.callback = callback

    # =====================================================
    # MESSAGE PARSER (FIX CORE BUG)
    # =====================================================
    def _handle_message(self, message):

        try:
            # 1) str → dict 변환
            if isinstance(message, str):
                try:
                    message = json.loads(message)
                except Exception:
                    logger.warning(f"WS non-json: {message}")
                    return

            # 2) 안전 타입 체크
            if not isinstance(message, dict):
                return

            data = message.get("data")
            if not data:
                return

            # 3) list / dict 대응
            if isinstance(data, list):
                for item in data:
                    self._extract(item)

            elif isinstance(data, dict):
                self._extract(data)

        except Exception as e:
            logger.error(f"WS parse error: {e}")

    # =====================================================
    # PRICE EXTRACTION SAFE
    # =====================================================
    def _extract(self, item):

        if not isinstance(item, dict):
            return

        try:
            price = item.get("lastPrice") or item.get("price")

            if price is None:
                return

            price = float(price)

            if self.callback:
                self.callback(price)

        except Exception as e:
            logger.error(f"extract error: {e}")

    # =====================================================
    # WS EVENTS
    # =====================================================
    def _on_message(self, ws, message):
        self._handle_message(message)

    def _on_error(self, ws, error):
        logger.error(f"WS error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        logger.warning("WebSocket closed")

    def _on_open(self, ws):
        logger.info("WebSocket connected")

        try:
            sub = {
                "op": "subscribe",
                "args": ["tickers.BTCUSDT"]
            }
            ws.send(json.dumps(sub))
        except Exception as e:
            logger.error(f"subscribe error: {e}")

    # =====================================================
    # START
    # =====================================================
    def start(self):

        def run():
            self.ws = websocket.WebSocketApp(
                self.url,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
                on_open=self._on_open
            )

            self.ws.run_forever()

        threading.Thread(target=run, daemon=True).start()

        logger.info("WebSocket started")


ws_client = BybitWebSocket()
