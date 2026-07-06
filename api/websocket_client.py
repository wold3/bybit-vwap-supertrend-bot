import json
import logging
import websocket
import threading

from services.event_bus import event_bus

logger = logging.getLogger(__name__)


class BybitWebSocket:

    def __init__(self):

        self.ws = None

    # =====================================================
    # START
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

        threading.Thread(target=run, daemon=True).start()

    # =====================================================
    # MESSAGE HANDLER (핵심 수정)
    # =====================================================
    def on_message(self, ws, message):

        try:

            # -------------------------
            # 1) 안전 파싱 (핵심)
            # -------------------------
            if isinstance(message, bytes):
                message = message.decode("utf-8")

            if not message:
                return

            data = json.loads(message)

            # -------------------------
            # 2) PRICE EVENT
            # -------------------------
            if "topic" in data and "tickers" in data.get("topic", ""):

                items = data.get("data", [])

                # 👉 str 방지 핵심
                if isinstance(items, list):

                    for item in items:

                        if not isinstance(item, dict):
                            continue

                        price = item.get("lastPrice")

                        if price is None:
                            continue

                        event_bus.publish({
                            "type": "PRICE",
                            "symbol": item.get("symbol"),
                            "price": float(price)
                        })

        except Exception as e:
            logger.error(f"WS message error: {str(e)}")

    # =====================================================
    # OPEN
    # =====================================================
    def on_open(self, ws):
        logger.info("WebSocket connected")

    # =====================================================
    # CLOSE
    # =====================================================
    def on_close(self, ws, *args):
        logger.warning("WebSocket closed")

    # =====================================================
    # ERROR
    # =====================================================
    def on_error(self, ws, error):
        logger.error(f"WebSocket error: {error}")


ws_client = BybitWebSocket()
