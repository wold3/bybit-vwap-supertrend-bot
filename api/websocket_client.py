import json
import logging
import websocket

logger = logging.getLogger(__name__)


class BybitWebSocket:

    def __init__(self):
        self.ws = None
        self.callback = None

    def set_price_callback(self, cb):
        self.callback = cb

    def on_message(self, ws, message):

        try:
            # =========================
            # 🔥 핵심 수정 (여기 중요)
            # =========================

            if isinstance(message, str):
                data = json.loads(message)
            else:
                data = message

            # Bybit 구조 안전 처리
            if isinstance(data, dict):

                # ticker / trade 구조 대응
                if "data" in data:
                    data = data["data"]

                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, str):
                            item = json.loads(item)

                        price = item.get("lastPrice") or item.get("price")

                        if price and self.callback:
                            self.callback(float(price))

                elif isinstance(data, dict):
                    price = data.get("lastPrice") or data.get("price")

                    if price and self.callback:
                        self.callback(float(price))

        except Exception as e:
            logger.error(f"WS message error: {str(e)}")

    def on_open(self, ws):
        logger.info("WebSocket connected")

    def on_close(self, ws):
        logger.warning("WebSocket closed")

    def start(self):
        logger.info("WebSocket started")

        self.ws = websocket.WebSocketApp(
            "wss://stream.bybit.com/v5/public/linear",
            on_message=self.on_message,
            on_open=self.on_open,
            on_close=self.on_close
        )

        self.ws.run_forever()
