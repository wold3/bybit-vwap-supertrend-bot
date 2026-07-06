import json
import logging
import websocket
import threading

logger = logging.getLogger(__name__)


class BybitWebSocket:

    def __init__(self):

        self.ws = None
        self.callback = None

    # =====================================================
    # callback 등록
    # =====================================================
    def set_price_callback(self, callback):
        self.callback = callback

    # =====================================================
    # 메시지 처리 (핵심 수정)
    # =====================================================
    def on_message(self, ws, message):

        try:
            # -----------------------------
            # 1. JSON 안전 파싱 (핵심)
            # -----------------------------
            if isinstance(message, bytes):
                message = message.decode("utf-8")

            if isinstance(message, str):
                try:
                    data = json.loads(message)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid WS string: {message}")
                    return
            else:
                data = message

            # -----------------------------
            # 2. Bybit 구조 대응
            # -----------------------------
            # 경우 1: {"data": {...}}
            if isinstance(data, dict) and "data" in data:
                data = data["data"]

            # 경우 2: list 구조
            if isinstance(data, list):
                for item in data:
                    self._handle_item(item)
                return

            # 경우 3: 단일 dict
            self._handle_item(data)

        except Exception as e:
            logger.error(f"WS message error safe handler: {str(e)}")

    # =====================================================
    # 실제 price 처리
    # =====================================================
    def _handle_item(self, item):

        try:
            if not isinstance(item, dict):
                return

            # Bybit ticker 대응
            price = None
            volume = None

            # 여러 구조 대응
            if "lastPrice" in item:
                price = float(item.get("lastPrice", 0))
                volume = float(item.get("volume24h", 0))

            elif "price" in item:
                price = float(item.get("price", 0))

            elif "data" in item:
                inner = item.get("data", {})
                if isinstance(inner, dict):
                    price = float(inner.get("price", 0))

            # callback 호출
            if price is not None and self.callback:
                self.callback(price)

        except Exception as e:
            logger.error(f"WS item error: {str(e)}")

    # =====================================================
    # 연결 이벤트
    # =====================================================
    def on_open(self, ws):
        logger.info("WebSocket connected")

    def on_close(self, ws, *args):
        logger.warning("WebSocket closed")

    def on_error(self, ws, error):
        logger.error(f"WebSocket error: {error}")

    # =====================================================
    # 시작
    # =====================================================
    def start(self):

        def run():

            self.ws = websocket.WebSocketApp(
                "wss://stream.bybit.com/v5/public/linear",
                on_message=self.on_message,
                on_open=self.on_open,
                on_close=self.on_close,
                on_error=self.on_error
            )

            logger.info("WebSocket started")
            self.ws.run_forever()

        t = threading.Thread(target=run, daemon=True)
        t.start()


# =====================================================
# SINGLETON
# =====================================================
ws_client = BybitWebSocket()
