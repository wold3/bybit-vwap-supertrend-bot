import logging
from datetime import datetime

from api.bybit_client import bybit_client

logger = logging.getLogger(__name__)


class OrderManager:

    def __init__(self):

        self.open_orders = {}
        self.filled_orders = {}

    # =====================================================
    # ORDER PLACE
    # =====================================================
    def place_market_order(self, symbol, side, qty, leverage=1):

        try:

            resp = bybit_client.place_order(
                symbol=symbol,
                side=side,
                qty=qty,
                leverage=leverage
            )

            # Bybit v5 safe parsing
            result = resp.get("result", {})
            order_id = result.get("orderId")

            if not order_id:
                logger.error(f"ORDER FAIL: {resp}")
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
            logger.error(f"ORDER ERROR: {e}")
            return None

    # =====================================================
    # SYNC ORDERS (실전용)
    # =====================================================
    def sync_orders(self):

        for order_id in list(self.open_orders.keys()):

            order = self.open_orders[order_id]

            # mock fill (실전에서는 execution API로 교체 가능)
            if (datetime.utcnow() - order["created_at"]).seconds > 2:

                order["status"] = "FILLED"

                self.filled_orders[order_id] = order
                del self.open_orders[order_id]

                logger.info(f"ORDER FILLED: {order_id}")

    # =====================================================
    # STATUS
    # =====================================================
    def status(self):

        return {
            "open": len(self.open_orders),
            "filled": len(self.filled_orders)
        }


order_manager = OrderManager()
