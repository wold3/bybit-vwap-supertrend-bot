import json
import logging
import threading
import websocket

logger = logging.getLogger(__name__)


class BybitWebSocket:

    def __init__(self):
        self.ws = None
        self.callback = None
        self.running = False

    # =========================
    # callback
    # =========================
    def set_price_callback(self, callback):
        self.callback = callback

    # =========================
    # message handler (FIX 핵심)
    # =========================
    def _on_message(self, ws, message):

        try:
            # 1) JSON 변환 (string 대비)
            if isinstance(message, str):
                try:
                    data = json.loads(message)
                except:
                    return
            else:
                data = message

            # 2) dict 아니면 종료
            if not isinstance(data, dict):
                return

            # 3) Bybit wrapper 제거
            if "data" in data:
                data = data["data"]

            # 4) list 대응
            if isinstance(data, list):
                if len(data) == 0:
                    return
                data = data[0]

            if not isinstance(data, dict):
                return

            # 5) price 추출 (안전)
            price = data.get("lastPrice") or data.get("price")

            if price is None:
                return

            try:
                price = float(price)
            except:
                return

            # 6) callback 실행
            if self.callback:
                self.callback(price, 0)

        except Exception as e:
            logger.error(f"WS message error: {str(e)}")

    # =========================
    # lifecycle
    # =========================
    def _on_open(self, ws):
        logger.info("WebSocket connected")

    def _on_close(self, ws, *args):
        logger.warning("WebSocket closed")

    def _on_error(self, ws, error):
        logger.error(f"WebSocket error: {error}")

    # =========================
    # start
    # =========================
    def start(self):

        url = "wss://stream.bybit.com/v5/public/linear"

        self.ws = websocket.WebSocketApp(
            url,
            on_message=self._on_message,
            on_open=self._on_open,
            on_close=self._on_close,
            on_error=self._on_error
        )

        self.running = True

        t = threading.Thread(target=self.ws.run_forever)
        t.daemon = True
        t.start()

        logger.info("WebSocket started")


ws_client = BybitWebSocket()
