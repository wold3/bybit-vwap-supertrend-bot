import json
import logging
import websocket

logger = logging.getLogger(__name__)


class BybitWebSocket:

    def __init__(self):
        self.ws = None
        self.price_callback = None

    def set_price_callback(self, callback):
        self.price_callback = callback

    # =========================
    # 메시지 처리 핵심 FIX
    # =========================
    def _on_message(self, ws, message):

        try:
            # ✅ 1) string이면 JSON 파싱
            if isinstance(message, str):
                try:
                    data = json.loads(message)
                except Exception:
                    logger.warning(f"WS non-json message skipped: {message}")
                    return
            else:
                data = message

            # ✅ 2) dict 아니면 종료
            if not isinstance(data, dict):
                logger.warning(f"WS invalid type skipped: {type(data)}")
                return

            # =========================
            # Bybit 구조 방어 처리
            # =========================

            if "data" in data:
                data = data["data"]

            # list 형태 방어
            if isinstance(data, list):
                for item in data:
                    self._process_item(item)
            else:
                self._process_item(data)

        except Exception as e:
            logger.error(f"WS message error: {str(e)}")

    # =========================
    # 실제 처리
    # =========================
    def _process_item(self, item):

        try:
            if not isinstance(item, dict):
                return

            price = None

            # 여러 Bybit 포맷 대응
            if "lastPrice" in item:
                price = float(item.get("lastPrice", 0))
            elif "price" in item:
                price = float(item.get("price", 0))
            elif "p" in item:
                price = float(item.get("p", 0))

            if price and self.price_callback:
                self.price_callback(price)

        except Exception as e:
            logger.error(f"WS item error: {str(e)}")

    def _on_open(self, ws):
        logger.info("WebSocket connected")

    def _on_close(self, ws, close_status_code, close_msg):
        logger.warning("WebSocket closed")

    def start(self):
        self.ws = websocket.WebSocketApp(
            "wss://stream.bybit.com/v5/public/linear",
            on_message=self._on_message,
            on_open=self._on_open,
            on_close=self._on_close
        )

        logger.info("WebSocket started")
        self.ws.run_forever()

    def stop(self):
        if self.ws:
            self.ws.close()
            logger.info("WebSocket stopped")


ws_client = BybitWebSocket()
