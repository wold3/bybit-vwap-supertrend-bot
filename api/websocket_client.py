import json
import time
import logging
import threading
import websocket

logger = logging.getLogger(__name__)


class BybitWebSocket:

    def __init__(self):

        self.ws = None
        self.callback = None
        self.last_ping = time.time()
        self.connected = False

    # =====================================================
    # callback
    # =====================================================
    def set_price_callback(self, callback):
        self.callback = callback

    # =====================================================
    # message handler
    # =====================================================
    def _on_message(self, ws, message):

        try:

            if isinstance(message, str):
                try:
                    data = json.loads(message)
                except:
                    return
            else:
                data = message

            if not isinstance(data, dict):
                return

            price = None
            volume = None

            if "data" in data:
                inner = data["data"]

                if isinstance(inner, list) and len(inner) > 0:
                    item = inner[0]
                    price = item.get("lastPrice") or item.get("price")
                    volume = item.get("volume24h")

            price = price or data.get("price")

            if price is None:
                return

            price = float(price)
            volume = float(volume or 0)

            if self.callback:
                self.callback(price, volume)

        except Exception as e:
            logger.error(f"WS message error: {str(e)}")

    # =====================================================
    # open
    # =====================================================
    def _on_open(self, ws):

        self.connected = True
        logger.info("WebSocket connected")

    # =====================================================
    # close
    # =====================================================
    def _on_close(self, ws, *args):

        self.connected = False
        logger.warning("WebSocket closed")

    # =====================================================
    # error
    # =====================================================
    def _on_error(self, ws, error):

        self.connected = False
        logger.error(f"WebSocket error: {error}")

    # =====================================================
    # run
    # =====================================================
    def _run(self):

        while True:

            try:

                self.ws = websocket.WebSocketApp(
                    "wss://stream.bybit.com/v5/public/linear",
                    on_message=self._on_message,
                    on_open=self._on_open,
                    on_close=self._on_close,
                    on_error=self._on_error,
                )

                self.ws.run_forever()

            except Exception as e:
                logger.error(f"WS crash: {str(e)}")

            # =================================================
            # reconnect delay
            # =================================================
            logger.info("Reconnecting WebSocket in 3 seconds...")
            time.sleep(3)

    # =====================================================
    # start
    # =====================================================
    def start(self):

        t = threading.Thread(target=self._run, daemon=True)
        t.start()

        logger.info("WebSocket started")

    # =====================================================
    # stop
    # =====================================================
    def stop(self):

        if self.ws:
            self.ws.close()
            logger.info("WebSocket stopped")


ws_client = BybitWebSocket()
