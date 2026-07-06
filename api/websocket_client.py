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
    # message handler (핵심 수정 부분)
    # =====================================================
    def _on_message(self, ws, message):

        try:
            # ----------------------------
            # 1. 문자열이면 JSON 변환
            # ----------------------------
            if isinstance(message, str):
                try:
                    data = json.loads(message)
                except Exception:
                    logger.warning(f"WS non-json message skipped: {message}")
                    return
            else:
                data = message

            # ----------------------------
            # 2. Bybit 구조 안전 처리
            # ----------------------------
            price = None
            volume = None

            # dict 아닐 경우 방어
            if not isinstance(data, dict):
                return

            # 여러 포맷 대응
            if "data" in data:
                inner = data.get("data")

                if isinstance(inner, list) and len(inner) > 0:
                    item = inner[0]

                    if isinstance(item, dict):
                        price = item.get("lastPrice") or item.get("price")
                        volume = item.get("volume24h")

                elif isinstance(inner, dict):
                    price = inner.get("lastPrice") or inner.get("price")

            # fallback
            price = price or data.get("price")

            if price is None:
                return

            price = float(price)
            volume = float(volume) if volume else 0

            # callback 실행
            if self.callback:
                self.callback(price, volume)

        except Exception as e:
            logger.error(f"WS message error: {str(e)}")

    # =====================================================
    # open
    # =====================================================
    def _on_open(self, ws):
        logger.info("WebSocket connected")

    # =====================================================
    # run
    # =====================================================
    def start(self):

        def run():
            self.ws = websocket.WebSocketApp(
                "wss://stream.bybit.com/v5/public/linear",
                on_message=self._on_message,
                on_open=self._on_open,
            )

            logger.info("WebSocket started")
            self.ws.run_forever()

        threading.Thread(target=run, daemon=True).start()

    def stop(self):
        if self.ws:
            self.ws.close()
            logger.info("WebSocket stopped")


ws_client = BybitWebSocket()
