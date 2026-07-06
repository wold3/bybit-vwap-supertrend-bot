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

    # =====================================================
    # 콜백 등록
    # =====================================================
    def set_price_callback(self, cb):
        self.callback = cb

    # =====================================================
    # 안전 JSON 파서
    # =====================================================
    def safe_parse(self, msg):
        if isinstance(msg, str):
            try:
                return json.loads(msg)
            except:
                return None
        return msg

    # =====================================================
    # 메시지 처리 (핵심)
    # =====================================================
    def on_message(self, ws, message):

        try:
            data = self.safe_parse(message)

            if not isinstance(data, dict):
                return

            # Bybit 구조 대응
            inner = data.get("data")

            if not inner:
                return

            # list 구조 대응
            if isinstance(inner, list):

                item = inner[0] if len(inner) > 0 else None

                if not isinstance(item, dict):
                    return

                # price 추출 (여러 키 대응)
                price = (
                    item.get("lastPrice")
                    or item.get("price")
                )

                if price is None:
                    return

                try:
                    price = float(price)
                except:
                    return

                if self.callback:
                    self.callback(price)

            # dict 구조 대응
            elif isinstance(inner, dict):

                price = inner.get("lastPrice") or inner.get("price")

                if price is None:
                    return

                try:
                    price = float(price)
                except:
                    return

                if self.callback:
                    self.callback(price)

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

        thread = threading.Thread(
            target=self.ws.run_forever,
            daemon=True
        )
        thread.start()

    # =====================================================
    def stop(self):
        self.running = False

        if self.ws:
            self.ws.close()

        logger.info("WebSocket stopped")


# 싱글톤 인스턴스
ws_client = BybitWebSocket()
