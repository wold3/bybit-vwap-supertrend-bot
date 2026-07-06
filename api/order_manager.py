import logging
from datetime import datetime

from api.bybit_client import bybit_client

logger = logging.getLogger(__name__)


class OrderManager:

    def __init__(self):
        self.open_orders = {}
        self.filled_orders = {}

    def place_market_order(self, symbol, side, qty, leverage=1):

        try:
            resp = bybit_client.place_order(
                symbol=symbol,
                side=side,
                qty=qty,
                leverage=leverage
            )

            if not isinstance(resp, dict):
                logger.error(f"Invalid response: {resp}")
                return None

            result = resp.get("result")
            if not isinstance(result, dict):
                logger.error(f"No result: {resp}")
                return None

            order_id = result.get("orderId")

            if not order_id:
                logger.error(f"Order failed: {resp}")
                return None

            self.open_orders[order_id] = {
                "symbol": symbol,
                "side": side,
                "qty": qty,
                "status": "PENDING",
                "created_at": datetime.utcnow()
            }

            logger.info(f"ORDER PLACED: {order_id}")

            return order_id

        except Exception as e:
            logger.error(f"Place order error: {str(e)}")
            return None


order_manager = OrderManager()
