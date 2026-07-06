import logging
from datetime import datetime

from api.bybit_client import bybit_client

logger = logging.getLogger(__name__)


class OrderManager:

    def __init__(self):
        self.open_orders = {}
        self.filled_orders = {}

    # =====================================================
    # 주문 생성
    # =====================================================
    def place_market_order(self, symbol, side, qty, leverage=1):

        try:
            resp = bybit_client.place_order(
                symbol=symbol,
                side=side,
                qty=qty,
                leverage=leverage
            )

            result = resp.get("result") or {}
            order_id = result.get("orderId")

            if not order_id:
                logger.error(f"Order failed: {resp}")
                return None

            self.open_orders[order_id] = {
                "symbol": symbol,
                "side": side,
                "qty": qty,
                "entry_price": None,   # 🔥 추가
                "status": "PENDING",
                "created_at": datetime.utcnow()
            }

            logger.info(f"ORDER PLACED: {order_id}")

            return order_id

        except Exception as e:
            logger.error(f"Place order error: {str(e)}")
            return None

    # =====================================================
    # 상태 체크
    # =====================================================
    def check_order_status(self, order_id, current_price=None):

        order = self.open_orders.get(order_id)
        if not order:
            return None

        # mock fill
        if (datetime.utcnow() - order["created_at"]).seconds > 2:

            order["status"] = "FILLED"
            order["entry_price"] = current_price  # 🔥 entry 저장

            self.filled_orders[order_id] = order
            del self.open_orders[order_id]

            return "FILLED"

        return "PENDING"

    # =====================================================
    # sync
    # =====================================================
    def sync_orders(self, current_price=None):

        for order_id in list(self.open_orders.keys()):
            status = self.check_order_status(order_id, current_price)

            if status == "FILLED":
                logger.info(f"ORDER FILLED: {order_id}")

    # =====================================================
    # PnL 계산용 데이터
    # =====================================================
    def get_filled_orders(self):
        return self.filled_orders

    # =====================================================
    # status
    # =====================================================
    def status(self):

        return {
            "open_orders": len(self.open_orders),
            "filled_orders": len(self.filled_orders)
        }


order_manager = OrderManager()
