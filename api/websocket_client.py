import json
import websocket
import threading
import logging
import time

from services.event_bus import event_bus

logger = logging.getLogger(__name__)


class WSClient:

    def start(self):

        t = threading.Thread(target=self.run, daemon=True)
        t.start()

    def run(self):

        while True:

            try:

                ws = websocket.WebSocketApp(
                    "wss://stream.bybit.com/v5/public/linear",
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close
                )

                ws.run_forever(ping_interval=20)

            except Exception as e:
                logger.error(f"WS crash: {e}")

            time.sleep(3)

    # ================================
    # SAFE PARSER (핵심)
    # ================================
    def on_message(self, ws, msg):

        try:

            # 1. string -> json
            if isinstance(msg, str):

                try:
                    data = json.loads(msg)
                except:
                    # pong / heartbeat 등
                    return
            else:
                data = msg

            # 2. 반드시 dict 체크
            if not isinstance(data, dict):
                return

            topic = data.get("topic", "")

            # 3. ticker만 처리
            if "tickers" not in topic:
                return

            # 4. data 안전 체크
            items = data.get("data", [])
            if not isinstance(items, list):
                return

            for item in items:

                if not isinstance(item, dict):
                    continue

                event_bus.put({
                    "type": "TICK",
                    "symbol": item.get("symbol"),
                    "price": float(item.get("lastPrice", 0))
                })

        except Exception as e:
            logger.error(f"WS message error: {e}")

    def on_error(self, ws, error):
        logger.error(f"WS error: {error}")

    def on_close(self, ws, code, msg):
        logger.warning(f"WS closed: {code} {msg}")


ws_client = WSClient()
