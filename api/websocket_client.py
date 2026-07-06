import json
import logging

logger = logging.getLogger(__name__)


class WebSocketClient:

    def __init__(self):
        self.callback = None

    def set_price_callback(self, cb):
        self.callback = cb

    def safe(self, msg):
        if isinstance(msg, str):
            try:
                return json.loads(msg)
            except:
                return None
        return msg

    def on_message(self, msg):

        try:
            data = self.safe(msg)

            if not isinstance(data, dict):
                return

            # BYBIT trade structure 대응
            if "data" in data:
                inner = data["data"]

                if isinstance(inner, list) and len(inner) > 0:
                    item = inner[0]

                    if isinstance(item, dict):
                        price = (
                            item.get("lastPrice")
                            or item.get("price")
                        )

                        if price and self.callback:
                            self.callback(float(price))

        except Exception as e:
            logger.error(f"WS error: {e}")
