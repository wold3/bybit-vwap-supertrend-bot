import json
import logging
import websocket
import threading

from api.order_manager import order_manager

logger = logging.getLogger(__name__)


class BybitWebSocket:

    def __init__(self):

        self.ws = None
        self.price_callback = None

    # =====================================================
    # PRICE CALLBACK
    # =====================================================
    def set_price_callback(self, callback):
        self.price_callback = callback

    # =====================================================
    # MESSAGE HANDLER
    # =====================================================
    def on_message(self, ws, message):

        try:

            if isinstance(message, bytes):
                message = message.decode("utf-8")

            data = json.loads(message)

            # =================================================
            # 1) PRICE STREAM
            # =================================================
            if "topic" in data and "tickers" in data.get("topic", ""):

                items = data.get("data", [])

                for item in items:

                    price = item.get("lastPrice")

                    if price and self.price_callback:
                        self.price_callback(float(price))

            # =================================================
            # 2) 🔥 EXECUTION STREAM (핵심 추가)
            # =================================================
            if "topic" in data and "execution" in data.get("topic", ""):

                executions = data.get("data", [])

                for exe in executions:
                    self._handle_fill(exe)

        except Exception as e:
            logger.error(f"WS error: {str(e)}")

    # =====================================================
    # 🔥 FILL HANDLER
    # =====================================================
    def _handle_fill(self, exe):

        try:

            order_id = exe.get("orderId")
            status = exe.get("execType")

            if not order_id:
                return

            # fill 확인
            if status in ["Trade", "BustTrade"]:

                if order_id in order_manager.open_orders:

                    order = order_manager.open_orders[order_id]

                    order["status"] = "FILLED"

                    order_manager.filled_orders[order_id] = order
                    del order_manager.open_orders[order_id]

                    logger.info(f"🔥 ORDER FILLED (WS): {order_id}")

        except Exception as e:
            logger.error(f"FILL ERROR: {str(e)}")

    # =====================================================
    # CONNECTION
    # =====================================================
    def on_open(self, ws):
        logger.info("WebSocket connected")

    def on_close(self, ws, *args):
        logger.warning("WebSocket closed")

    def on_error(self, ws, error):
        logger.error(f"WebSocket error: {error}")

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

        t = threading.Thread(target=run, daemon=True)
        t.start()


ws_client = BybitWebSocket()
