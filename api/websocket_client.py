import json
import threading
import websocket
import logging

logger = logging.getLogger(__name__)


class BybitWebSocket:

    def __init__(self, symbol="BTCUSDT"):

        self.symbol = symbol
        self.ws_url = "wss://stream.bybit.com/v5/public/linear"

        self.price_callback = None
        self.volume_callback = None

        self.ws = None
        self.running = False

    # =====================================================
    # ON MESSAGE
    # =====================================================

    def _on_message(self, ws, message):

        try:
            data = json.loads(message)

            if "data" not in data:
                return

            for item in data["data"]:

                price = float(item.get("lastPrice", 0))
                volume = float(item.get("volume24h", 0))

                if self.price_callback:
                    self.price_callback(price)

                if self.volume_callback:
                    self.volume_callback(volume)

        except Exception as e:
            logger.error(f"WS message error: {str(e)}")

    # =====================================================
    # ON ERROR
    # =====================================================

    def _on_error(self, ws, error):

        logger.error(f"WS error: {error}")

    # =====================================================
    # ON CLOSE
    # =====================================================

    def _on_close(self, ws, close_status_code, close_msg):

        logger.warning("WebSocket closed")

        if self.running:
            logger.info("Reconnecting...")
            self.start()

    # =====================================================
    # ON OPEN
    # =====================================================

    def _on_open(self, ws):

        logger.info("WebSocket connected")

        sub_msg = {
            "op": "subscribe",
            "args": [
                f"tickers.{self.symbol}"
            ]
        }

        ws.send(json.dumps(sub_msg))

    # =====================================================
    # START
    # =====================================================

    def start(self):

        self.running = True

        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )

        thread = threading.Thread(
            target=self.ws.run_forever,
            daemon=True
        )

        thread.start()

        logger.info("WebSocket started")

    # =====================================================
    # STOP
    # =====================================================

    def stop(self):

        self.running = False

        if self.ws:
            self.ws.close()

        logger.info("WebSocket stopped")

    # =====================================================
    # CALLBACKS
    # =====================================================

    def set_price_callback(self, func):

        self.price_callback = func

    def set_volume_callback(self, func):

        self.volume_callback = func


# =====================================================
# SINGLETON
# =====================================================

ws_client = BybitWebSocket()
