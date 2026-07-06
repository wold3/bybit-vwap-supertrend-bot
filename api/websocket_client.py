import json
import time
import websocket
import threading
import logging

from services.event_bus import event_bus

logger = logging.getLogger(__name__)


class WSClient:

    def __init__(self):

        self.ws = None
        self.running = True
        self.last_ping = time.time()

    # =====================================================
    # START
    # =====================================================
    def start(self):

        t = threading.Thread(target=self._run, daemon=True)
        t.start()

        logger.info("WebSocket started")

    # =====================================================
    # MAIN LOOP (AUTO RECONNECT)
    # =====================================================
    def _run(self):

        while self.running:

            try:

                self.ws = websocket.WebSocketApp(
                    "wss://stream.bybit.com/v5/public/linear",
                    on_open=self.on_open,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close
                )

                self.ws.run_forever(
                    ping_interval=20,
                    ping_timeout=10
                )

            except Exception as e:
                logger.error(f"WS crash: {e}")

            logger.info("WS reconnect in 3 sec...")
            time.sleep(3)

    # =====================================================
    # OPEN
    # =====================================================
    def on_open(self, ws):

        logger.info("WebSocket connected")

        self.last_ping = time.time()

    # =====================================================
    # MESSAGE
    # =====================================================
    def on_message(self, ws, msg):

        try:

            if isinstance(msg, str):
                data = json.loads(msg)
            else:
                data = msg

            if not isinstance(data, dict):
                return

            topic = data.get("topic", "")

            if "tickers" in topic:

                for item in data.get("data", []):

                    if not isinstance(item, dict):
                        continue

                    event_bus.put({
                        "type": "TICK",
                        "symbol": item.get("symbol"),
                        "price": float(item.get("lastPrice", 0))
                    })

        except Exception as e:
            logger.error(f"WS message error: {e}")

    # =====================================================
    # ERROR
    # =====================================================
    def on_error(self, ws, error):

        logger.error(f"WS error: {error}")

    # =====================================================
    # CLOSE
    # =====================================================
    def on_close(self, ws, code, msg):

        logger.warning(f"WS closed: {code} {msg}")


ws_client = WSClient()
